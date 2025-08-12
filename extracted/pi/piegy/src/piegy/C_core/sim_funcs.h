/**
 * This .h defines the simulation functions in piegy.simulation
*/

#ifndef SIM_FUNCS
#define SIM_FUNCS

#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>
#include <math.h>

#include "patch.h"
#include "model.h"
#include "random.h"





// directions of migration
// so that 3 - mig_dir = reflection of it. Used to track neighbors
// the actual implementation of signals still uses this order: up, down, left, right
#define MIG_UP 0
#define MIG_DOWN 1
#define MIG_LEFT 2
#define MIG_RIGHT 3
#define NO_MIG 4

// results of single_test
#define SUCCESS 0
#define DATA_NOT_EMPTY 1
#define SMALL_MAXTIME 2
#define SIM_OVERFLOW 3
#define ACCURACY_ERROR 4


/**
 * Handling Numerical Errors:
 * half of the rates / values related to rates are calculated on a cumulative basis. i.e., updated over time instead of re-calculating from scratch
 * numerival errors might explode in this case, so need to re-calculate every sometime
*/

// where exp(x) is considered overflow
// below the actual bound (709) to preserve accuracy
#define EXP_OVERFLOW_BOUND 500

// Compare current rates with this bound
#define ACCURATE_BOUND 1ULL << 53

// how frequent to update rates & sum of rates in single test (recalculate)
#define UPDATE_SUM_ROUNDS_SM 100U  // small, more frequent if some rate is larger than ACCURATE_BOUND
#define UPDATE_SUM_ROUNDS_LG 10000U


/**
 * index of patch in find_patch
*/
typedef struct patch_picked_t {
    size_t i;
    size_t j;
    double current_sum;
} patch_picked_t;

/**
 * index & event number in make_signal_*
*/
typedef struct signal_t {
    // relative location of the second patch to the first
    // set to NO_MIG if the event only affects one patch
    // otherwise set to MIG_* constants as defined above
    uint8_t rela_loc;

    // the first patch
    size_t i1;
    size_t j1;
    size_t ij1;  // i1 * M + j1
    uint8_t e1;

    // the second patch
    size_t i2;
    size_t j2;
    size_t ij2;
    uint8_t e2;
} signal_t;



/**
 * Defined in .c
*/
static void find_nb_zero_flux(size_t* restrict nb, size_t i, size_t j, size_t N, size_t M, size_t NM);
static void find_nb_periodical(size_t* restrict nb, size_t i, size_t j, size_t N, size_t M, size_t NM);
static double single_init(const model_t* restrict mod, patch_t* restrict world, size_t* restrict nb_indices, 
                    double* restrict patch_rates, double* restrict sum_rates_by_row, double* restrict sum_rates_p, 
                    signal_t* restrict sig_p, patch_picked_t* restrict picked_p);
static uint8_t single_test(model_t* restrict mod, char* message);
static void single_test_free(patch_t** world, size_t** nb_indices, double** patch_rates, double** sum_rates_by_row);
uint8_t run(model_t* restrict mod, char* message, size_t msg_len);



/**
 * patch functions
*/

static inline void update_pi_k(patch_t* restrict p) {
    // update payoff and carrying capacity rates 
    uint32_t U = p->U_ph;
    uint32_t V = p->V_ph;
    double sum = U + V;

    if (sum > 0) {
        double U_ratio = U / sum;
        double V_ratio = V / sum;
        if (U > 0) {
            p->Hpi_ph = U_ratio * p->matirx[0] + V_ratio * p->matirx[1];
        } else {
            p->Hpi_ph = 0.0;
        }

        if (V > 0) {
            p->Dpi_ph = U_ratio * p->matirx[2] + V_ratio * p->matirx[3];
        } else {
            p->Dpi_ph = 0.0;
        }

    } else {
        p->Hpi_ph = 0.0;
        p->Dpi_ph = 0.0;
    }

    p->pi_death_rates[0] = fabs(U * p->Hpi_ph);
    p->pi_death_rates[1] = fabs(V * p->Dpi_ph);

    p->pi_death_rates[2] = p->params[4] * U * sum;
    p->pi_death_rates[3] = p->params[5] * V * sum;

    p->sum_pi_death_rates = 0.0;
    for (size_t i = 0; i < 4; i++) {
        p->sum_pi_death_rates += p->pi_death_rates[i];
    }
}



static inline void update_mig_just_rate(patch_t* restrict p) {
    // update migration weight for patch p, in location loc. Only rate is updated
    // used by last-changed patch, when there is only one last-changed patch
    double* p_H_weight = p->H_weight;
    double* p_D_weight = p->D_weight;

    double mu1_U = p->params[0] * p->U_ph;
    double mu2_V = p->params[1] * p->V_ph;
    
    double mu1_U_divide_sum = mu1_U / p->sum_H_weight;
    double mu2_V_divide_sum = mu2_V / p->sum_D_weight;

    for (size_t i = 0; i < 4; i++) {
        p->mig_rates[i] = mu1_U_divide_sum * p_H_weight[i];
        p->mig_rates[i + 4] = mu2_V_divide_sum * p_D_weight[i];
    }
    p->sum_mig_rates = mu1_U + mu2_V;
}


static inline uint8_t update_mig_weight_rate(patch_t* restrict p, const uint8_t loc) {
    // update migration weight as well as rates, in one direction
    // used by neighbors of last-changed patches
    // also used by last-changed patches themselve, when there are two patch changed, to update mig rates of in each other's direction

    double* p_H_weight = p->H_weight;
    double* p_D_weight = p->D_weight;

    patch_t* nbi = p->nb[loc];
    p->sum_H_weight -= p_H_weight[loc];
    p->sum_D_weight -= p_D_weight[loc];

    double w1_Hpi = p->params[2] * nbi->Hpi_ph;
    double w2_Dpi = p->params[3] * nbi->Dpi_ph;
    if (w1_Hpi > EXP_OVERFLOW_BOUND) {
        return SIM_OVERFLOW;
    }
    if (w2_Dpi > EXP_OVERFLOW_BOUND) {
        return SIM_OVERFLOW;
    }

    switch(loc) {
        case MIG_UP:
            p_H_weight[MIG_UP] = exp(w1_Hpi);
            p_D_weight[MIG_UP] = exp(w2_Dpi);
            break;
        case MIG_DOWN:
            p_H_weight[MIG_DOWN] = exp(w1_Hpi);
            p_D_weight[MIG_DOWN] = exp(w2_Dpi);
            break;
        case MIG_LEFT:
            p_H_weight[MIG_LEFT] = exp(w1_Hpi);
            p_D_weight[MIG_LEFT] = exp(w2_Dpi);
            break;
        default:
            p_H_weight[MIG_RIGHT] = exp(w1_Hpi);
            p_D_weight[MIG_RIGHT] = exp(w2_Dpi);
            break;
    }
    p->sum_H_weight += p_H_weight[loc];
    p->sum_D_weight += p_D_weight[loc];

    double mu1_U = p->params[0] * p->U_ph;
    double mu2_V = p->params[1] * p->V_ph;
    double mu1_U_divide_sum = mu1_U / p->sum_H_weight;
    double mu2_V_divide_sum = mu2_V / p->sum_D_weight;

    for (size_t i = 0; i < 4; i++) {
        p->mig_rates[i] = mu1_U_divide_sum * p_H_weight[i];
        p->mig_rates[i + 4] = mu2_V_divide_sum * p_D_weight[i];
    }
    p->sum_mig_rates = mu1_U + mu2_V;

    return SUCCESS;
}



static inline uint8_t init_mig(patch_t* restrict p) {
    // update migration rate for all directions

    double* p_H_weight = p->H_weight;
    double* p_D_weight = p->D_weight;

    p->sum_H_weight = 0.0;
    p->sum_D_weight = 0.0;

    double w1 = p->params[2];
    double w2 = p->params[3];

    for (size_t i = 0; i < 4; i++) {
        patch_t* nbi = p->nb[i];
        if (nbi) {
            // not NULL
            double w1_Hpi = w1 * nbi->Hpi_ph;
            double w2_Dpi = w2 * nbi->Dpi_ph;
            if (w1_Hpi > EXP_OVERFLOW_BOUND) {
                return SIM_OVERFLOW;
            }
            if (w2_Dpi > EXP_OVERFLOW_BOUND) {
                return SIM_OVERFLOW;
            }
            p_H_weight[i] = exp(w1_Hpi);
            p_D_weight[i] = exp(w2_Dpi);

            p->sum_H_weight += p_H_weight[i];
            p->sum_D_weight += p_D_weight[i];
        }
    }

    double mu1_U = p->params[0] * p->U_ph;
    double mu2_V = p->params[1] * p->V_ph;
    double mu1_U_divide_sum = mu1_U / p->sum_H_weight;
    double mu2_V_divide_sum = mu2_V / p->sum_D_weight;

    for (size_t i = 0; i < 4; i++) {
        p->mig_rates[i] = mu1_U_divide_sum * p_H_weight[i];
        p->mig_rates[i + 4] = mu2_V_divide_sum * p_D_weight[i];
    }
    p->sum_mig_rates = mu1_U + mu2_V;

    return SUCCESS;
}



static inline uint8_t find_event(const patch_t* restrict p, const double expected_sum) {
    size_t event = 0;
    double current_sum;

    //if (expected_sum > (p->sum_pi_death_rates + p->sum_mig_rates)) {
    //    fprintf(stderr, "Bug: patch rate not enough in find_event.\n");
    //}

    if (expected_sum < p->sum_pi_death_rates) {
        // First 4 events (payoff and death)
        current_sum = 0.0;
        while (current_sum < expected_sum) {
            current_sum += p->pi_death_rates[event];
            event++;
        }
        event--;  // step back to correct event index
    } else {
        // Last 8 events (migration)2
        current_sum = p->sum_pi_death_rates;
        while (current_sum < expected_sum) {
            current_sum += p->mig_rates[event];
            event++;
        }
        event += 3;  // -1 and then +4
    }

    return event;
}


static inline void change_popu(patch_t* restrict p, const uint8_t s) {
    switch (s) {
        case 0:
            // Migration IN for U
            p->U_ph += 1;
            return;
        case 1:
            // Migration OUT / death due to carrying capacity for U
            p->U_ph -= (p->U_ph > 0);
            return;
        case 2:
            // Natural birth/death for U due to payoff
            if (p->Hpi_ph > 0) {
                p->U_ph += 1;
            } else if (p->U_ph > 0) {
                p->U_ph -= 1;
            }
            return;
        case 3:
            // Migration IN for V
            p->V_ph += 1;
            return;
        case 4:
            // Migration OUT / death due to carrying capacity for V
            p->V_ph -= (p->V_ph > 0);
            return;
        default:
            // Natural birth/death for V due to payoff
            if (p->Dpi_ph > 0) {
                p->V_ph += 1;
            } else if (p->V_ph > 0) {
                p->V_ph -= 1;
            }
            return;
    }
}


/**
 * Main Simulation Functions
*/

static inline void find_patch(patch_picked_t* restrict picked, const double expected_sum, 
                                const double* restrict patch_rates, const double* restrict sum_rates_by_row, const double sum_rates, const size_t N, const size_t M) {
    double current_sum = 0;
    size_t row = 0;
    size_t col = 0;
    size_t row_M = 0;

    // Find row
    if (N != 1) {
        if (expected_sum < sum_rates * 0.5) {
            current_sum = 0.0;
            row = 0;
            while (current_sum < expected_sum) {
                current_sum += sum_rates_by_row[row];
                row++;
            }
            row--;
            current_sum -= sum_rates_by_row[row];
        } else {
            current_sum = sum_rates;
            row = N - 1;
            while (current_sum > expected_sum) {
                current_sum -= sum_rates_by_row[row];
                row--;
            }
            row++;
        }
        row_M = row * M;
    }

    // Find col in that row
    if ((expected_sum - current_sum) < sum_rates_by_row[row] * 0.5) {
        col = 0;
        while (current_sum < expected_sum) {
            current_sum += patch_rates[row_M + col];
            col++;
        }
        col--;
        current_sum -= patch_rates[row_M + col];
    } else {
        current_sum += sum_rates_by_row[row];
        col = M - 1;
        while (current_sum > expected_sum) {
            current_sum -= patch_rates[row_M + col];
            col--;
        }
        col++;
    }

    picked->i = row;
    picked->j = col;
    picked->current_sum = current_sum;
}



static inline void make_signal_zero_flux(const size_t N, const size_t M, const size_t i, const size_t j, const uint8_t e, signal_t* restrict signal) {
    // pass in N & M as well to match the param set of make_signal_periodical
    (void) N;
    (void) M;
    // this is always the case for the first one
    signal->i1 = i;
    signal->j1 = j;

    switch (e) {
        case 0:
            signal->e1 = 2;
            signal->rela_loc = NO_MIG;
            return;
        case 1:
            signal->e1 = 5;
            signal->rela_loc = NO_MIG;
            return;
        case 2:
            signal->e1 = 1;
            signal->rela_loc = NO_MIG;
            return;
        case 3:
            signal->e1 = 4;
            signal->rela_loc = NO_MIG;
            return;
        case 4:
            signal->e1 = 1;
            signal->i2 = i - 1;
            signal->j2 = j;
            signal->e2 = 0;
            signal->rela_loc = MIG_UP;
            return;
        case 5:
            signal->e1 = 1;
            signal->i2 = i + 1;
            signal->j2 = j;
            signal->e2 = 0;
            signal->rela_loc = MIG_DOWN;
            return;
        case 6:
            signal->e1 = 1;
            signal->i2 = i;
            signal->j2 = j - 1;
            signal->e2 = 0;
            signal->rela_loc = MIG_LEFT;
            return;
        case 7:
            signal->e1 = 1;
            signal->i2 = i;
            signal->j2 = j + 1;
            signal->e2 = 0;
            signal->rela_loc = MIG_RIGHT;
            return;
        case 8:
            signal->e1 = 4;
            signal->i2 = i - 1;
            signal->j2 = j;
            signal->e2 = 3;
            signal->rela_loc = MIG_UP;
            return;
        case 9:
            signal->e1 = 4;
            signal->i2 = i + 1;
            signal->j2 = j;
            signal->e2 = 3;
            signal->rela_loc = MIG_DOWN;
            return;
        case 10:
            signal->e1 = 4;
            signal->i2 = i;
            signal->j2 = j - 1;
            signal->e2 = 3;
            signal->rela_loc = MIG_LEFT;
            return;
        default:
            signal->e1 = 4;
            signal->i2 = i;
            signal->j2 = j + 1;
            signal->e2 = 3;
            signal->rela_loc = MIG_RIGHT;
            return;
    }
}



static inline void make_signal_periodical(const size_t N, const size_t M, const size_t i, const size_t j, const uint8_t e, signal_t* restrict signal) {
    // this is always the case for the first one
    signal->i1 = i;
    signal->j1 = j;

    switch (e) {
        case 0:
            signal->e1 = 2;
            signal->rela_loc = NO_MIG;
            return;
        case 1:
            signal->e1 = 5;
            signal->rela_loc = NO_MIG;
            return;
        case 2:
            signal->e1 = 1;
            signal->rela_loc = NO_MIG;
            return;
        case 3:
            signal->e1 = 4;
            signal->rela_loc = NO_MIG;
            return;
        case 4:
            signal->e1 = 1;
            signal->i2 = i != 0 ? i - 1 : N - 1;
            signal->j2 = j;
            signal->e2 = 0;
            signal->rela_loc = MIG_UP;
            return;
        case 5:
            signal->e1 = 1;
            signal->i2 = i != N - 1 ? i + 1 : 0;
            signal->j2 = j;
            signal->e2 = 0;
            signal->rela_loc = MIG_DOWN;
            return;
        case 6:
            signal->e1 = 1;
            signal->i2 = i;
            signal->j2 = j != 0 ? j - 1 : M - 1;
            signal->e2 = 0;
            signal->rela_loc = MIG_LEFT;
            return;
        case 7:
            signal->e1 = 1;
            signal->i2 = i;
            signal->j2 = j != M - 1 ? j + 1 : 0;
            signal->e2 = 0;
            signal->rela_loc = MIG_RIGHT;
            return;
        case 8:
            signal->e1 = 4;
            signal->i2 = i != 0 ? i - 1 : N - 1;
            signal->j2 = j;
            signal->e2 = 3;
            signal->rela_loc = MIG_UP;
            return;
        case 9:
            signal->e1 = 4;
            signal->i2 = i != N - 1 ? i + 1 : 0;
            signal->j2 = j;
            signal->e2 = 3;
            signal->rela_loc = MIG_DOWN;
            return;
        case 10:
            signal->e1 = 4;
            signal->i2 = i;
            signal->j2 = j != 0 ? j - 1 : M - 1;
            signal->e2 = 3;
            signal->rela_loc = MIG_LEFT;
            return;
        default:
            signal->e1 = 4;
            signal->i2 = i;
            signal->j2 = j != M - 1 ? j + 1 : 0;
            signal->e2 = 3;
            signal->rela_loc = MIG_RIGHT;
            return;
    }
}


#endif
