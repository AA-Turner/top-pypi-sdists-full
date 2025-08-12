/**
 * This .c includes the patch struct and "member functions" 
 * that correponds to patch class in piegy.model module
*/

#include "patch.h"

void patch_init(patch_t* p, uint32_t U_ph, uint32_t V_ph, double* X_start, double* P_start) {
    if (p == NULL) return;

    p->U_ph = (double) U_ph;
    p->V_ph = (double) V_ph;
    p->Hpi_ph = 0;
    p->Dpi_ph = 0;

    memcpy(p->matirx, X_start, 4 * sizeof(double));
    memcpy(p->params, P_start, 6 * sizeof(double));

    for (size_t i = 0; i < 4; i++) {
        p->H_weight[i] = 0;
        p->D_weight[i] = 0;
        p->pi_death_rates[i] = 0;
    }
    for (size_t i = 0; i < 8; i++) {
        p->mig_rates[i] = 0;
    }
    p->sum_H_weight = 0;
    p->sum_D_weight = 0;
    p->sum_pi_death_rates = 0;
    p->sum_mig_rates = 0;
}


void set_nb(patch_t* world, size_t* nb_start, size_t ij, size_t NM) {
    // nb_start is the where patch ij's neighbor indices start
    size_t num_nb = 0;
    for (size_t k = 0; k < 4; k++) {
        if (nb_start[k] != NM) {
            // neighbor is valid
            world[ij].nb[k] = &world[nb_start[k]];
            num_nb += 1;
        } else {
            world[ij].nb[k] = NULL;
        }
    }
    world[ij].params[0] *= (0.25 * num_nb);
    world[ij].params[1] *= (0.25 * num_nb);
}
