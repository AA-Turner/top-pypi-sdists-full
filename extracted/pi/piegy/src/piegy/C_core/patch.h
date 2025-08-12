/**
 * This .h includes the patch struct and "member functions" 
 * that correponds to patch class in piegy.model module
*/

#ifndef PATCH_H
#define PATCH_H

#include <math.h>
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>


typedef struct patch_t {
    double U_ph;    // store as double directly to avoid runtime conversion (into double)
                    // "ph" refers to "patch", population/payoff of current patch
    double V_ph;
    double Hpi_ph;
    double Dpi_ph;

    double matirx[4];  // a copy of matrix and patch variables (mu, w, kappa)
    double params[6];  // patch parameters of the current patch

    double H_weight[4];  // stores migration weight of each of the 4 neighbors
    double D_weight[4];
    double sum_H_weight; // sum of H_weight
    double sum_D_weight;
    double pi_death_rates[4];
    double mig_rates[8];
    double sum_pi_death_rates;
    double sum_mig_rates;

    struct patch_t* nb[4];
} patch_t;

// in .c
void patch_init(patch_t* p, uint32_t U, uint32_t V, double* X_start, double* P_start);
void set_nb(patch_t* world, size_t* nb_start, size_t ij, size_t NM) ;

#endif // PATCH_H

