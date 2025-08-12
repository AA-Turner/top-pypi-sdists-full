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
                const uint32_t* init_popu, const double* matrices, const double* patch_params,
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
    mod->init_popu = (uint32_t*) malloc(sizeof(uint32_t) * NM * 2);
    mod->matrices = (double*) malloc(sizeof(double) * NM * 4);
    mod->patch_params = (double*) malloc(sizeof(double) * NM * 6);

    if (!mod->init_popu || !mod->matrices || !mod->patch_params) return false;

    memcpy(mod->init_popu, init_popu, sizeof(uint32_t) * NM * 2);
    memcpy(mod->matrices, matrices, sizeof(double) * NM * 4);
    memcpy(mod->patch_params, patch_params, sizeof(double) * NM * 6);

    // Data
    mod->data_empty = true;
    mod->max_record = (size_t)(mod->maxtime / mod->record_itv);
    mod->arr_size = NM * mod->max_record;
    mod->compress_itv = 1;

    mod->U1d     = (double*) calloc(mod->arr_size, sizeof(double));
    mod->V1d     = (double*) calloc(mod->arr_size, sizeof(double));
    mod->Hpi_1d  = (double*) calloc(mod->arr_size, sizeof(double));
    mod->Dpi_1d  = (double*) calloc(mod->arr_size, sizeof(double));

    if (!mod->U1d || !mod->V1d || !mod->Hpi_1d || !mod->Dpi_1d) {
        fprintf(stdout, "Error: allocating memory in mod_init.\n");
        fflush(stdout);
        exit(EXIT_FAILURE);
    }

    return true;
}



void mod_free(model_t* mod) {
    if (!mod) return;

    free(mod->init_popu);
    free(mod->matrices);
    free(mod->patch_params);
    free(mod->U1d);
    free(mod->V1d);
    free(mod->Hpi_1d);
    free(mod->Dpi_1d);
    mod->init_popu = NULL;
    mod->matrices = mod->patch_params = mod->U1d = mod->V1d = mod->Hpi_1d = mod->Dpi_1d = NULL;

    free(mod);
}


void mod_free_py(model_t* mod) {
    // free function for python
    // the same as mod_free except for not having free(mod)
    if (!mod) return;

    free(mod->init_popu);
    free(mod->matrices);
    free(mod->patch_params);
    free(mod->U1d);
    free(mod->V1d);
    free(mod->Hpi_1d);
    free(mod->Dpi_1d);
    mod->init_popu = NULL;
    mod->matrices = mod->patch_params = mod->U1d = mod->V1d = mod->Hpi_1d = mod->Dpi_1d = NULL;
}


void calculate_ave(model_t* mod) {
    if (mod->sim_time == 1) return;

    for (size_t i = 0; i < mod->arr_size; i++) {
        mod->U1d[i]    /= mod->sim_time;
        mod->V1d[i]    /= mod->sim_time;
        mod->Hpi_1d[i] /= mod->sim_time;
        mod->Dpi_1d[i] /= mod->sim_time;
    }
}

