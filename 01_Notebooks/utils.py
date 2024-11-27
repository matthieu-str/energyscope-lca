def get_impact_scores(impact_category, df_impact_scores, df_results):
    impact_scores_cat = df_impact_scores[df_impact_scores.Impact_category == str(impact_category)]

    df_lifetime = df_results.parameters['lifetime'].reset_index()

    df_f_mult = df_results.variables['F_Mult'].reset_index()
    df_f_mult = df_f_mult.merge(impact_scores_cat[impact_scores_cat.Type == 'Construction'][['Name', 'Value']],
                                left_on='index', right_on='Name', how='left')
    df_f_mult = df_f_mult.merge(df_lifetime[['index', 'lifetime']], on='index', how='left')
    df_f_mult[impact_category[-1]] = df_f_mult.F_Mult * df_f_mult.Value / df_f_mult.lifetime

    df_annual_prod = df_results.variables['Annual_Prod'].reset_index()
    df_annual_prod = df_annual_prod.merge(impact_scores_cat[impact_scores_cat.Type == 'Operation'][['Name', 'Value']],
                                          left_on='index', right_on='Name', how='left')
    df_annual_prod[impact_category[-1]] = df_annual_prod.Annual_Prod * df_annual_prod.Value

    df_annual_res = df_results.variables['Annual_Res'].reset_index()
    df_annual_res = df_annual_res.merge(impact_scores_cat[impact_scores_cat.Type == 'Resource'][['Name', 'Value']],
                                        left_on='index', right_on='Name', how='left')
    df_annual_res[impact_category[-1]] = df_annual_res.Annual_Res * df_annual_res.Value

    return df_f_mult, df_annual_prod, df_annual_res
