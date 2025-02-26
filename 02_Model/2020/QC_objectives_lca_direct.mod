
set INDICATORS;

param lcia_op {INDICATORS,TECHNOLOGIES} default 0;
var LCIA_op {INDICATORS,TECHNOLOGIES};
var TotalLCIA {INDICATORS} >= 0;

# LCIA operation
subject to lcia_op_calc {id in INDICATORS, i in TECHNOLOGIES}:
  LCIA_op[id,i] >= lcia_op[id,i] * sum {t in PERIODS} (t_op[t] * F_Mult_t[i, t]);

subject to totalLCIA_calc_r {id in INDICATORS}:
  TotalLCIA[id] = sum {i in TECHNOLOGIES} LCIA_op[id,i];

var TotalLCIA_TTHH;
subject to LCIA_TTHH_cal:
  TotalLCIA_TTHH = TotalLCIA['TTHH'] + TotalCost*1e-6;

var TotalLCIA_TTEQ;
subject to LCIA_TTEQ_cal:
  TotalLCIA_TTEQ = TotalLCIA['TTEQ'] + TotalCost*1e-6;

var TotalLCIA_m_CCS;
subject to LCIA_m_CCS_cal:
  TotalLCIA_m_CCS = TotalLCIA['m_CCS'] + TotalCost*1e-6;

