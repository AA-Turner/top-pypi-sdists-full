/**
 * This .h includes the model struct and "member functions" 
 * that correpond to patch class in piegy.model module
*/
#ifndef MODEL_H
#define MODEL_H

#include <stdbool.h>
#include <stdlib.h>
#include <stdint.h>


typedef struct model_t {
    size_t N;
    size_t M;
    double maxtime;
    double record_itv;
    size_t sim_time;

    bool boundary;

    // 3D arrays flattened to 1D for C
    // Sizes: N * M * 2, N * M * 4, N * M * 6
    uint32_t* I;
    double* X;
    double* P;

    int32_t print_pct; 
    int32_t seed;  // -1 for none

    // vars for data storage
    bool data_empty;
    size_t max_record;
    size_t arr_size;  // size of U, V, U_pi, V_pi, equals N * M * max_record
    uint32_t compress_itv;
    double* U1d;
    double* V1d;
    double* Upi_1d;
    double* Vpi_1d;
} model_t;


bool mod_init(model_t* mod, size_t N, size_t M,
                double maxtime, double record_itv, size_t sim_time, bool boundary,
                const uint32_t* I, const double* X, const double* P,
                int32_t print_pct, int32_t seed);
void mod_free(model_t* mod);
void mod_free_py(model_t* mod);
void calculate_ave(model_t* mod);



#endif // MODEL_H

