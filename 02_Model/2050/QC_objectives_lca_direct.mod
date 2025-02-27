
param direct_op {INDICATORS,TECHNOLOGIES} default 0;
param limit_direct {INDICATORS} default 1e10;
var DIRECT_op {INDICATORS,TECHNOLOGIES};
var TotalDIRECT {INDICATORS} >= 0;

# Operation
subject to direct_op_calc {id in INDICATORS, i in TECHNOLOGIES}:
  DIRECT_op[id,i] >= direct_op[id,i] * sum {t in PERIODS} (t_op[t] * F_Mult_t[i, t]);

subject to totalDIRECT_calc_r {id in INDICATORS}:
  TotalDIRECT[id] = sum {i in TECHNOLOGIES} DIRECT_op[id,i];

subject to totalDIRECT_limit {id in INDICATORS}:
  TotalDIRECT[id] <= limit_direct[id];

var TotalDIRECT_TTHH;
subject to DIRECT_TTHH_cal:
  TotalDIRECT_TTHH = TotalDIRECT['TTHH'] + TotalCost*1e-6;

var TotalDIRECT_TTEQ;
subject to DIRECT_TTEQ_cal:
  TotalDIRECT_TTEQ = TotalDIRECT['TTEQ'] + TotalCost*1e-6;

var TotalDIRECT_m_CCS;
subject to DIRECT_m_CCS_cal:
  TotalDIRECT_m_CCS = TotalDIRECT['m_CCS'] + TotalCost*1e-6;

