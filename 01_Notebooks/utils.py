import pandas as pd
import ast


def get_impact_scores(
        impact_category: str or list[str],
        df_impact_scores: pd.DataFrame,
        df_results: pd.DataFrame,
        assessment_type: str = 'esm',
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    if isinstance(impact_category, str):
        impact_category = [impact_category]

    if type(df_impact_scores.Impact_category.iloc[0]) is tuple:
        pass
    elif type(df_impact_scores.Impact_category.iloc[0]) is str:
        df_impact_scores.Impact_category = df_impact_scores.Impact_category.apply(lambda x: ast.literal_eval(x))

    df_lifetime = df_results.parameters['lifetime'].reset_index()
    df_f_mult = df_results.variables['F_Mult'].reset_index()
    df_f_mult = df_f_mult.merge(df_lifetime[['index', 'lifetime']], on='index', how='left')
    df_annual_prod = df_results.variables['Annual_Prod'].reset_index()
    df_annual_res = df_results.variables['Annual_Res'].reset_index()

    for cat in impact_category:
        impact_scores_cat = df_impact_scores[df_impact_scores.Impact_category == cat]

        if assessment_type == 'esm':
            df_f_mult = df_f_mult.merge(impact_scores_cat[impact_scores_cat.Type == 'Construction'][['Name', 'Value']],
                                        left_on='index', right_on='Name', how='left')
            df_f_mult[cat[-1]] = df_f_mult.F_Mult * df_f_mult.Value / df_f_mult.lifetime
            df_f_mult.drop(columns=['Name', 'Value'], inplace=True)

            df_annual_res = df_annual_res.merge(impact_scores_cat[impact_scores_cat.Type == 'Resource'][['Name', 'Value']],
                                                left_on='index', right_on='Name', how='left')
            df_annual_res[cat[-1]] = df_annual_res.Annual_Res * df_annual_res.Value
            df_annual_res.drop(columns=['Name', 'Value'], inplace=True)

        df_annual_prod = df_annual_prod.merge(impact_scores_cat[impact_scores_cat.Type == 'Operation'][['Name', 'Value']],
                                              left_on='index', right_on='Name', how='left')
        df_annual_prod[cat[-1]] = df_annual_prod.Annual_Prod * df_annual_prod.Value
        df_annual_prod.drop(columns=['Name', 'Value'], inplace=True)

    if assessment_type == 'esm':
        return df_f_mult, df_annual_prod, df_annual_res
    else:
        return df_annual_prod


def get_life_cycle_phase_impact_per_capita(
        df_f_mult: pd.DataFrame,
        df_annual_prod: pd.DataFrame,
        df_annual_res: pd.DataFrame,
        df_annual_prod_direct: pd.DataFrame,
        impact_category: str,
        N_capita: int,
        N_digits: int = 3,
) -> tuple[float, float, float, float, float]:
    operation = df_annual_prod[impact_category].sum() / N_capita
    construction = df_f_mult[impact_category].sum() / N_capita
    resource = df_annual_res[impact_category].sum() / N_capita
    total_from_impact_scores = operation + construction + resource

    operation_direct = df_annual_prod_direct[impact_category].sum() / N_capita

    if impact_category == 'Climate change, short term':
        total_from_impact_scores *= 1e-3  # Convert from kg CO2-eq to t CO2-eq
        operation *= 1e-3
        construction *= 1e-3
        resource *= 1e-3
        operation_direct *= 1e-3

    unit = get_impact_category_unit(impact_category)
    print(f'Life-cycle carbon footprint per capita: {round(total_from_impact_scores, N_digits)} {unit} / capita')
    print(f'Percentage due to operation: {round(operation / total_from_impact_scores * 100, N_digits)} %')
    print(f'Including direct emissions: {round(operation_direct / total_from_impact_scores * 100, N_digits)} %')
    print(f'Percentage due to construction: {round(construction / total_from_impact_scores * 100, N_digits)} %')
    print(f'Percentage due to resource: {round(resource / total_from_impact_scores * 100, N_digits)} %')

    return total_from_impact_scores, operation, construction, resource, operation_direct


def get_life_cycle_phase_cost_per_capita(
        df_results: pd.DataFrame,
        N_capita: int,
        N_digits: int = 3,
) -> tuple[float, float, float, float]:
    df_c_inv_an = pd.merge(
        left=df_results.variables['C_inv'],
        right=df_results.parameters['tau'],
        left_index=True,
        right_index=True,
    )

    df_c_inv_an['C_inv_an'] = df_c_inv_an['C_in'] * df_c_inv_an['tau']
    total_cost = 1e6 * float(df_results.variables['TotalCost'].TotalCost.iloc[0]) / N_capita

    maintenance_cost = 1e6 * df_results.variables['C_maint'].C_maint.sum() / N_capita
    operation_cost = 1e6 * df_results.variables['C_op'].C_op.sum() / N_capita
    annualized_investment_cost = 1e6 * df_c_inv_an['C_inv_an'].sum() / N_capita

    print(f'Total cost: {int(total_cost)} CAD / cap / year')
    print(f'Maintenance cost ratio: {round(100 * maintenance_cost / total_cost, N_digits)} %')
    print(f'Operation cost ratio: {round(100 * operation_cost / total_cost, N_digits)} %')
    print(f'Annualized investment cost ratio: {round(100 * annualized_investment_cost / total_cost, N_digits)} %')

    return total_cost, maintenance_cost, operation_cost, annualized_investment_cost


def get_impact_category_unit(
        impact_category: str,
) -> str:
    if impact_category == 'Climate change, short term':
        return 't CO2-eq'
    elif impact_category == 'Total human health':
        return 'DALY'
    elif impact_category == 'Total ecosystem quality':
        return 'PDF.m2.yr'
    else:
        raise ValueError(f"Unknown impact category: {impact_category}")


def get_contribution_df(
        df: pd.DataFrame,
        impact_category: str,
        N: int = 5,
        n_run: int = 0,
) -> pd.DataFrame:
    df = df[df.Run == n_run]
    df = df.sort_values(impact_category, ascending=False)
    total = df[impact_category].sum()
    df = df.head(N).reset_index(drop=True)
    total_in_top_N = df[impact_category].sum()
    df = df[['Run', 'index', impact_category]]
    df.loc[len(df)] = [n_run, 'OTHER', total - total_in_top_N]
    df[f'{impact_category} (ratio)'] = df[impact_category] / total
    return df
