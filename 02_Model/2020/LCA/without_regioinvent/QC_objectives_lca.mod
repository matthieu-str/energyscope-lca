
set INDICATORS;

param lcia_constr {INDICATORS,TECHNOLOGIES} default 0;
param lcia_op {INDICATORS,TECHNOLOGIES} default 0;
param lcia_res {INDICATORS, RESOURCES} default 0;
param limit_lcia {INDICATORS} default 1e10;
param refactor {INDICATORS} default 1;
var LCIA_constr {INDICATORS,TECHNOLOGIES};
var LCIA_op {INDICATORS,TECHNOLOGIES};
var LCIA_res {INDICATORS,RESOURCES};
var TotalLCIA {INDICATORS} >= 0;

# Construction
subject to lcia_constr_calc {id in INDICATORS, i in TECHNOLOGIES}:
  LCIA_constr[id,i] = (1/refactor[id]) * lcia_constr[id,i] * F_Mult[i];

# Operation
subject to lcia_op_calc {id in INDICATORS, i in TECHNOLOGIES}:
  LCIA_op[id,i] = lcia_op[id,i] * sum {t in PERIODS} (t_op[t] * F_Mult_t[i, t]);

# Resources
subject to lcia_res_calc {id in INDICATORS, r in RESOURCES}:
  LCIA_res[id,r] = lcia_res[id,r] * sum {t in PERIODS} (t_op[t] * F_Mult_t[r, t]);

subject to totalLCIA_calc_r {id in INDICATORS}:
  TotalLCIA[id] = sum {i in TECHNOLOGIES} (LCIA_constr[id,i] / lifetime[i]  + LCIA_op[id,i]) + sum{r in RESOURCES} (LCIA_res[id,r]);

subject to totalLCIA_limit {id in INDICATORS}:
  TotalLCIA[id] <= limit_lcia[id];

var TotalLCIA_TTHH;
subject to LCIA_TTHH_cal:
  TotalLCIA_TTHH = TotalLCIA['TTHH'] + TotalCost*1e-6;

var TotalLCIA_TTEQ;
subject to LCIA_TTEQ_cal:
  TotalLCIA_TTEQ = TotalLCIA['TTEQ'] + TotalCost*1e-6;

var TotalLCIA_m_CCS;
subject to LCIA_m_CCS_cal:
  TotalLCIA_m_CCS = TotalLCIA['m_CCS'] + TotalCost*1e-6;

