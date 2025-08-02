/**
 * This .c includes the model struct and "member functions" 
 * that correponds to patch class in piegy.model module
*/

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdbool.h>

#include "model.h"


bool mod_init(model_t* mod, size_t N, size_t M,
                double maxtime, double record_itv, size_t sim_time, bool boundary,
                const uint32_t* I, const double* X, const double* P,
                int32_t print_pct, int32_t seed) {

    mod->N = N;
    mod->M = M;
    mod->maxtime = maxtime;
    mod->record_itv = record_itv;
    mod->sim_time = sim_time;
    mod->boundary = boundary;
    mod->print_pct = print_pct;
    mod->seed = seed;

    size_t NM = N * M;

    // I, X, P
    mod->I = (uint32_t*) malloc(sizeof(uint32_t) * NM * 2);
    mod->X = (double*) malloc(sizeof(double) * NM * 4);
    mod->P = (double*) malloc(sizeof(double) * NM * 6);

    if (!mod->I || !mod->X || !mod->P) return false;

    memcpy(mod->I, I, sizeof(uint32_t) * NM * 2);
    memcpy(mod->X, X, sizeof(double) * NM * 4);
    memcpy(mod->P, P, sizeof(double) * NM * 6);

    // Data
    mod->data_empty = true;
    mod->max_record = (size_t)(mod->maxtime / mod->record_itv);
    mod->arr_size = NM * mod->max_record;
    mod->compress_itv = 1;

    mod->U1d     = (double*) calloc(mod->arr_size, sizeof(double));
    mod->V1d     = (double*) calloc(mod->arr_size, sizeof(double));
    mod->Upi_1d  = (double*) calloc(mod->arr_size, sizeof(double));
    mod->Vpi_1d  = (double*) calloc(mod->arr_size, sizeof(double));

    if (!mod->U1d || !mod->V1d || !mod->Upi_1d || !mod->Vpi_1d) {
        fprintf(stdout, "Error: allocating memory in mod_init.\n");
        fflush(stdout);
        exit(EXIT_FAILURE);
    }

    return true;
}



void mod_free(model_t* mod) {
    if (!mod) return;

    free(mod->I);
    free(mod->X);
    free(mod->P);
    free(mod->U1d);
    free(mod->V1d);
    free(mod->Upi_1d);
    free(mod->Vpi_1d);
    mod->I = NULL;
    mod->X = mod->P = mod->U1d = mod->V1d = mod->Upi_1d = mod->Vpi_1d = NULL;

    free(mod);
}


void mod_free_py(model_t* mod) {
    // free function for python
    // the same as mod_free except for not having free(mod)
    if (!mod) return;

    free(mod->I);
    free(mod->X);
    free(mod->P);
    free(mod->U1d);
    free(mod->V1d);
    free(mod->Upi_1d);
    free(mod->Vpi_1d);
    mod->I = NULL;
    mod->X = mod->P = mod->U1d = mod->V1d = mod->Upi_1d = mod->Vpi_1d = NULL;
}


void calculate_ave(model_t* mod) {
    if (mod->sim_time == 1) return;

    for (size_t i = 0; i < mod->arr_size; i++) {
        mod->U1d[i]    /= mod->sim_time;
        mod->V1d[i]    /= mod->sim_time;
        mod->Upi_1d[i] /= mod->sim_time;
        mod->Vpi_1d[i] /= mod->sim_time;
    }
}

