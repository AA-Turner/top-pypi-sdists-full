/* Two independent double-precision contacts per AArch64 Advanced SIMD vector.
 * Reuses packet scheduling and mixed-joint synchronization; no HastySpace threads.
 * Four logical lanes are solved in independent halves, with scalar odd tails. */
#include "cpContactSolver.h"
#if CP_NEON_CONTACT_SOLVER && CP_USE_DOUBLES
#include <arm_neon.h>
typedef float64x2_t V;
static inline V add(V a,V b){return vaddq_f64(a,b);}
static inline V sub(V a,V b){return vsubq_f64(a,b);}
static inline V mul(V a,V b){return vmulq_f64(a,b);}
static inline V neg(V a){return vnegq_f64(a);}
static inline V zero(void){return vdupq_n_f64(0.0);}
/* Match cpfmin/cpfmax: on equality or unordered comparison choose operand b.
 * Hardware fmin/fmax have different signed-zero/NaN selection semantics. */
static inline V vmin(V a,V b){return vbslq_f64(vcltq_f64(a,b),a,b);}
static inline V vmax(V a,V b){return vbslq_f64(vcgtq_f64(a,b),a,b);}
static inline void getAoS(const double *v,const int *ids,V *x,V *y,V *w,V *bx,V *by,V *bw){
 const double *a=v+6*ids[0],*b=v+6*ids[1];
 V a0=vld1q_f64(a),b0=vld1q_f64(b),a1=vld1q_f64(a+2),b1=vld1q_f64(b+2),a2=vld1q_f64(a+4),b2=vld1q_f64(b+4);
 *x=vzip1q_f64(a0,b0);*y=vzip2q_f64(a0,b0);
 *w=vzip1q_f64(a1,b1);*bx=vzip2q_f64(a1,b1);
 *by=vzip1q_f64(a2,b2);*bw=vzip2q_f64(a2,b2);
}
static inline void putAoS(double *v,const int *ids,int lanes,V x,V y,V w,V bx,V by,V bw){
 /* Exactly six doubles per body: no allocation padding or frozen-side writes. */
 double *a=v+6*ids[0];
 vst1q_f64(a,vzip1q_f64(x,y));vst1q_f64(a+2,vzip1q_f64(w,bx));vst1q_f64(a+4,vzip1q_f64(by,bw));
 if(lanes>1){double *b=v+6*ids[1];
  vst1q_f64(b,vzip2q_f64(x,y));vst1q_f64(b+2,vzip2q_f64(w,bx));vst1q_f64(b+4,vzip2q_f64(by,bw));}
}
#define load(p) vld1q_f64((p)+lane)
#define store(p,v) vst1q_f64((p)+lane,(v))
#include "cpContactSolverKernel.inc"
#undef load
#undef store
#include "cpContactSolverScalar.inc"

void
cpContactSolverKernelNeon(cpContactSolverContext *s,int iterations)
{
 for(int iteration=0;iteration<iterations;++iteration){
  for(int i=0;i<s->packetCount;++i){
   cpContactSolverPacket *p=&s->packets[i];
   for(int lane=0;lane<p->lanes;lane+=2){
    if(p->lanes-lane==1) solveScalarPacket(s,p,lane);
    else solvePacket(s,p,lane);
   }
  }
 }
}
#endif
