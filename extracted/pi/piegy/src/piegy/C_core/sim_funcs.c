/**
 * This .c defines the simulation functions in piegy.simulation
*/

#include <stdbool.h>
#include <time.h>

#include "sim_funcs.h"
#include "patch.h"
#include "model.h"



static void find_nb_zero_flux(size_t* restrict nb, size_t i, size_t j, size_t N, size_t M, size_t NM) {
    // Up
    if (i != 0) {
        nb[0] = (i - 1) * M + j;
    } else {
        nb[0] = NM;  // N * M for nb doesn't exist
    }

    // Down
    if (i != N - 1) {
        nb[1] = (i + 1) * M + j;
    } else {
        nb[1] = NM;
    }

    // Left
    if (j != 0) {
        nb[2] = i * M + j - 1;
    } else {
        nb[2] = NM;
    }

    // Right
    if (j != M - 1) {
        nb[3] = i * M + j + 1;
    } else {
        nb[3] = NM;
    }
}


static void find_nb_periodical(size_t* restrict nb, size_t i, size_t j, size_t N, size_t M, size_t NM) {
    // up
    if (N != 1) {
        nb[0] = (i != 0) ? (i - 1) * M + j : (N - 1) * M + j;
    } else {
        nb[0] = NM;
    }

    // down
    if (N != 1) {
        nb[1] = (i != N - 1) ? (i + 1) * M + j : j;
    } else {
        nb[1] = NM;
    }

    // We explicitly asked for M > 1
    // left
    nb[2] = (j != 0) ? i * M + j - 1 : i * M + M - 1;

    // right
    nb[3] = (j != M - 1) ? i * M + j + 1 : i * M;
}



// single_init function: initializes world, runs 1 event, returns updated variables
static double single_init(const model_t* restrict mod, patch_t* restrict world, size_t* restrict nb_indices, 
                    double* restrict patch_rates, double* restrict sum_rates_by_row, double* restrict sum_rates_p, 
                    signal_t* restrict sig_p, patch_picked_t* restrict picked_p) {

    size_t N = mod->N;
    size_t M = mod->M;
    size_t NM = N * M;
    size_t max_record = mod->max_record;
    size_t ij_out = 0;  // used to track index i * M + j in double for loops, "out" means not the "looper" in for loop

    // init world
    for (size_t i = 0; i < N; i++) {
        for (size_t j = 0; j < M; j++) {
            patch_init(&world[ij_out], mod->init_popu[ij_out * 2], mod->init_popu[ij_out * 2 + 1], &(mod->matrices[ij_out * 4]), &(mod->patch_params[ij_out * 6]));
            ij_out++;
        }
    }

    // init nb_indices
    ij_out = 0;
    if (mod->boundary) {
        for (size_t i = 0; i < N; i++) {
            for (size_t j = 0; j < M; j++) {
                find_nb_zero_flux(&nb_indices[ij_out * 4], i, j, N, M, NM);
                ij_out++;
            }
        }
    } else {
        for (size_t i = 0; i < N; i++) {
            for (size_t j = 0; j < M; j++) {
                find_nb_periodical(&nb_indices[ij_out * 4], i, j, N, M, NM);
                ij_out++;
            }
        }
    }


    // set nb pointers for patches
    for (size_t ij = 0; ij < NM; ij++) {
        set_nb(world, &nb_indices[ij * 4], ij, NM);
    }

    //////// Begin Running ////////

    // init payoff & natural death rates
    for (size_t ij = 0; ij < N; ij++) {
        update_pi_k(&world[ij]);
    }

    // init migration rates & store patch rates
    ij_out = 0;
    for (size_t i = 0; i < N; i++) {
        for (size_t j = 0; j < M; j++) {
            uint8_t mig_result = init_mig(&world[ij_out]);  // init mig rates for all 4 directions
            if (mig_result == SIM_OVERFLOW) {
                return -1 * SIM_OVERFLOW;
            }
            double ij_rates = world[ij_out].sum_pi_death_rates + world[ij_out].sum_mig_rates;
            patch_rates[ij_out] = ij_rates;
            sum_rates_by_row[i] += ij_rates;
            *sum_rates_p = *sum_rates_p + ij_rates;  // can't do *sum_rates_p += ij_rates
            ij_out++;
        }
    }

    // pick the first random event
    double expected_sum = random01() * *sum_rates_p;
    find_patch(picked_p, expected_sum, patch_rates, sum_rates_by_row, *sum_rates_p, N, M);
    size_t picked_idx = picked_p->i * M + picked_p->j;
    size_t e0 = find_event(&world[picked_idx], expected_sum - picked_p->current_sum);
    if (picked_idx >= NM || e0 >= 12) {
        return -1 * ACCURACY_ERROR;
    }

    // make signal
    if (mod->boundary) {
        make_signal_zero_flux(N, M, picked_p->i, picked_p->j, e0, sig_p); 
    } else {
        make_signal_periodical(N, M, picked_p->i, picked_p->j, e0, sig_p);
    }
    sig_p->ij1 = sig_p->i1 * M + sig_p->j1;
    sig_p->ij2 = sig_p->i2 * M + sig_p->j2; 

    // update patch based on signal
    change_popu(&world[sig_p->ij1], sig_p->e1);
    if (sig_p->rela_loc != NO_MIG) {
        change_popu(&world[sig_p->ij2], sig_p->e2);
    }

    // time increment
    double time = (1.0 / *sum_rates_p) * log(1.0 / random01());

    if (time > mod->maxtime) {
        // maxtime too small
        return -1 * SMALL_MAXTIME;
    }
    
    // store data
    if (time > mod->record_itv) {
        size_t recod_idx = (size_t) (time / mod->record_itv);

        for (size_t ij = 0; ij < NM; ij++) {
            size_t ij_max_record = ij * max_record;
            for (size_t k = 0; k < recod_idx; k++) {
                mod->U1d[ij_max_record + k] += world[ij].U_ph;
                mod->V1d[ij_max_record + k] += world[ij].V_ph;
                mod->Hpi_1d[ij_max_record + k] += world[ij].Hpi_ph;
                mod->Dpi_1d[ij_max_record + k] += world[ij].Dpi_ph;
            }
        }
    }

    return time;
}



static uint8_t single_test(model_t* restrict mod, char* message) {
    // bring some dimensions to the front
    size_t N = mod->N;
    size_t M = mod->M;
    size_t NM = N * M;
    double maxtime = mod->maxtime;
    size_t max_record = mod->max_record;
    double record_itv = mod->record_itv;
    bool boundary = mod->boundary;
    double* mod_U1d = mod->U1d;
    double* mod_V1d = mod->V1d;
    double* mod_Hpi_1d = mod->Hpi_1d;
    double* mod_Dpi_1d = mod->Dpi_1d;

    // update sum of rates every 1e5 rounds
    // many rates are updated each time, rather than re-calculated. 
    // So need to re-calculate from scratch every some rounds to reduce numerical errors
    size_t curr_update_sum_round = 0;  // current round
    size_t update_sum_freq = UPDATE_SUM_ROUNDS_SM;  // recalculate sum every this many rounds

    // set make_signal function based on boundary conditions
    void (*make_signal)(size_t, size_t, size_t, size_t, uint8_t, signal_t*);
    if (mod->boundary) {
        make_signal = &make_signal_zero_flux;
    } else {
        make_signal = &make_signal_periodical;
    }

    // core containers
    patch_t* world = (patch_t*) calloc(NM, sizeof(patch_t));
    size_t* nb_indices = (size_t*) calloc(NM * 4, sizeof(size_t));
    double* patch_rates = (double*) calloc(NM, sizeof(double));
    double* sum_rates_by_row = (double*) calloc(N, sizeof(double));
    double sum_rates = 0;

    signal_t signal;
    patch_picked_t picked;

    // print progress
    double one_progress = one_progress = 2.0 * maxtime;
    if (mod->print_pct != -1) {
        one_progress = maxtime * mod->print_pct / 100.0;
        fprintf(stdout, "\r                     ");
        fprintf(stdout, "\r%s: 0 %%", message);
        fflush(stdout);
    }
    double current_progress = one_progress;

    // Call single_init. Initialize rates and run for 1 event
    double time = single_init(mod, world, nb_indices, patch_rates, sum_rates_by_row, &sum_rates, &signal, &picked);
    if (time == -1 * SMALL_MAXTIME) {
        // time too small
        fprintf(stdout, "\nError: maxtime too small.\n");
        fflush(stdout);
        single_test_free(&world, &nb_indices, &patch_rates,  &sum_rates_by_row);
        return SMALL_MAXTIME;
    } else if (time == -1 * SIM_OVERFLOW) {
        fprintf(stdout, "\nError: overflow at t = 0\n");
        fflush(stdout);
        single_test_free(&world, &nb_indices, &patch_rates,  &sum_rates_by_row);
        return SIM_OVERFLOW;
    } else if (time == -1 * ACCURACY_ERROR) {
            fprintf(stdout, "\nError: accuracy too low at time 0, simulation stopped\n");
            fflush(stdout);
            single_test_free(&world, &nb_indices, &patch_rates,  &sum_rates_by_row);
            return ACCURACY_ERROR;
    }
    size_t record_index = (size_t) (time / mod->record_itv);
    double record_time = time - record_index * record_itv;

    ////////  while loop  ////////

    while (time < maxtime) {

        // update sums and print progress
        curr_update_sum_round++;
        if (curr_update_sum_round > update_sum_freq) {
            curr_update_sum_round = 0;

            // Print progress
            if (time > current_progress) {
                uint8_t curr_prog = (uint8_t)(time * 100 / maxtime);
                if (curr_prog < 10) {
                    fprintf(stdout, "\r%s: %d %%", message, (int)(time * 100 / maxtime));
                    fflush(stdout);
                } else {
                    fprintf(stdout, "\r%s: %d%%", message, (int)(time * 100 / maxtime));
                    fflush(stdout);
                }
                //fprintf(stdout, "\n99: %d, %d, %f, %f\n100: %d, %d, %f, %f\n", 
                //world[98].U, world[98].V, world[98].mig_rates[3], world[98].mig_rates[7], world[99].U, world[99].V, world[99].mig_rates[2], world[99].mig_rates[6]);
                //fflush(stdout);
                current_progress += one_progress;
            }

            // update sum
            update_sum_freq = UPDATE_SUM_ROUNDS_LG;  // assume can make it larger
            for (size_t ij = 0; ij < NM; ij++) {
                double sum_H_weight = 0;
                double sum_D_weight = 0;
                for (size_t k = 0; k < 4; k++) {
                    sum_H_weight += world[ij].H_weight[k];
                    sum_D_weight += world[ij].D_weight[k];
                }
                if (sum_H_weight > ACCURATE_BOUND || sum_D_weight > ACCURATE_BOUND) {
                    update_sum_freq = UPDATE_SUM_ROUNDS_SM;  // values too large, put back the small update frequency
                }
                world[ij].sum_H_weight = sum_H_weight;
                world[ij].sum_D_weight = sum_D_weight;
                // patch_rates are updated every time a patch is changed
            }
            size_t ij_out = 0;
            sum_rates = 0;
            for (size_t i = 0; i < N; i++) {
                double sum_rates_by_row_i = 0;
                for (size_t j = 0; j < M; j++) {
                    sum_rates_by_row_i += patch_rates[ij_out];
                    ij_out++;
                }
                sum_rates_by_row[i] = sum_rates_by_row_i;
                sum_rates += sum_rates_by_row_i;
            }
        }

        // update last-changed patches
        // subtract old rates first, then update patch, then add new rates
        // and split into cases whether there are two or one last-changed patches (because need to update all payoffs first and then mig rates)
        size_t si1 = signal.i1;
        size_t si2 = signal.i2;
        size_t sij1 = signal.ij1;
        size_t sij2 = signal.ij2;
        uint8_t rela_loc = signal.rela_loc;

        if (rela_loc == NO_MIG) {
            // if only one
            sum_rates_by_row[si1] -= patch_rates[sij1];
            sum_rates -= patch_rates[sij1];

            update_pi_k(&world[sij1]);
            update_mig_just_rate(&world[sij1]);

            patch_rates[sij1] = world[sij1].sum_pi_death_rates + world[sij1].sum_mig_rates;
            sum_rates_by_row[si1] += patch_rates[sij1];
            sum_rates += patch_rates[sij1];
        } else {
            // two
            sum_rates_by_row[si1] -= patch_rates[sij1];
            sum_rates_by_row[si2] -= patch_rates[sij2];
            sum_rates -= patch_rates[sij1];
            sum_rates -= patch_rates[sij2];

            update_pi_k(&world[sij1]);  // update both patches' payoffs first
            update_pi_k(&world[sij2]);

            if (update_mig_weight_rate(&world[sij1], rela_loc) == SIM_OVERFLOW || 
                update_mig_weight_rate(&world[sij2], rela_loc ^ 1) == SIM_OVERFLOW) {

                fprintf(stdout, "\nError: overflow at time %f\n", time);
                fflush(stdout);
                single_test_free(&world, &nb_indices, &patch_rates,  &sum_rates_by_row);
                return SIM_OVERFLOW;
            }

            patch_rates[sij1] = world[sij1].sum_pi_death_rates + world[sij1].sum_mig_rates;
            patch_rates[sij2] = world[sij2].sum_pi_death_rates + world[sij2].sum_mig_rates;
            sum_rates_by_row[si1] += patch_rates[sij1];
            sum_rates_by_row[si2] += patch_rates[sij2];
            sum_rates += patch_rates[sij1];
            sum_rates += patch_rates[sij2];
        }

        // update neighbors of last-changed patches
        if (rela_loc == NO_MIG) {
            for (uint8_t k = 0; k < 4; k++) {
                size_t nb_idx = nb_indices[sij1 * 4 + k];
                if (nb_idx == NM) { continue; }  // invalid neighbor
                // all neighbors, as long as exists, need to change
                if (update_mig_weight_rate(&world[nb_idx], k ^ 1) == SIM_OVERFLOW) {
                    fprintf(stdout, "\nError: overflow at t = %f\n", time);
                    fflush(stdout);
                    single_test_free(&world, &nb_indices, &patch_rates,  &sum_rates_by_row);
                    return SIM_OVERFLOW;
                }
                // patch_rates, and sums of rates is not changed
            }
        } else {
            // the first patch
            for (uint8_t k = 0; k < 4; k++) {
                size_t nb_idx = nb_indices[sij1 * 4 + k];
                if (nb_idx == NM) { continue; }
                if (k != rela_loc) {
                    // nb_idx isn't the second last-changed patch
                    if (update_mig_weight_rate(&world[nb_idx], k ^ 1) == SIM_OVERFLOW) {
                        fprintf(stdout, "\nError: overflow at t = %f\n", time);
                        fflush(stdout);
                        single_test_free(&world, &nb_indices, &patch_rates,  &sum_rates_by_row);
                        return SIM_OVERFLOW;
                    }
                }
            }
            // the second patch
            for (uint8_t k = 0; k < 4; k++) {
                size_t nb_idx = nb_indices[sij2 * 4 + k];
                if (nb_idx == NM) { continue; }
                if (k != (rela_loc ^ 1)) {
                    // nb_idx isn't the first last-changed patch
                    if (update_mig_weight_rate(&world[nb_idx], k ^ 1) == SIM_OVERFLOW) {
                        fprintf(stdout, "\nError: overflow at t = %f\n", time);
                        fflush(stdout);
                        single_test_free(&world, &nb_indices, &patch_rates,  &sum_rates_by_row);
                        return SIM_OVERFLOW;
                    }
                }
            }
        }

        // pick a random event
        double expected_sum = random01() * sum_rates;
        find_patch(&picked, expected_sum, patch_rates, sum_rates_by_row, sum_rates, N, M);
        size_t picked_idx = picked.i * M + picked.j;
        uint8_t e0 = find_event(&world[picked_idx], expected_sum - picked.current_sum);
        if (picked_idx >= NM || e0 >= 12) {
            fprintf(stdout, "\nError: accuracy too low at t = %f, simulation stopped\n", time);
            fflush(stdout);
            single_test_free(&world, &nb_indices, &patch_rates,  &sum_rates_by_row);
            return ACCURACY_ERROR;
        }

        // make signal
        (*make_signal)(N, M, picked.i, picked.j, e0, &signal);
        signal.ij1 = signal.i1 * M + signal.j1;
        signal.ij2 = signal.i2 * M + signal.j2;

        // let the event happenn
        change_popu(&world[signal.ij1], signal.e1);
        if (signal.rela_loc != NO_MIG) {
            change_popu(&world[signal.ij2], signal.e2);
        }

        // increase time
        double dt = (1.0 / sum_rates) * log(1.0 / random01());
        time += dt;
        record_time += dt;

        // record data
        if (time < maxtime) {
            if (record_time > record_itv) {
                size_t multi_records = record_time / record_itv;
                record_time -= multi_records * record_itv;
                size_t upper = record_index + multi_records;

                for (size_t ij = 0; ij < NM; ij++) {
                    size_t ij_max_record = ij * max_record;
                    for (size_t k = record_index; k < upper; k++) {
                        mod_U1d[ij_max_record + k] += world[ij].U_ph;
                        mod_V1d[ij_max_record + k] += world[ij].V_ph;
                        mod_Hpi_1d[ij_max_record + k] += world[ij].Hpi_ph;
                        mod_Dpi_1d[ij_max_record + k] += world[ij].Dpi_ph;
                    }
                }
                record_index += multi_records;
            }

        } else {
            // if already exceeds maxtime
            for (size_t ij = 0; ij < NM; ij++) {
                size_t ij_max_record = ij * max_record;
                for (size_t k = record_index; k < max_record; k++) {
                    mod_U1d[ij_max_record + k] += world[ij].U_ph;
                    mod_V1d[ij_max_record + k] += world[ij].V_ph;
                    mod_Hpi_1d[ij_max_record + k] += world[ij].Hpi_ph;
                    mod_Dpi_1d[ij_max_record + k] += world[ij].Dpi_ph;
                }
            }
        }
    }

    //////// End of while loop ////////

    /*if (mod->print_pct != -1) {
        fprintf(stdout, "\r%s: 100%%", message);
        fflush(stdout);
    }*/

    single_test_free(&world, &nb_indices, &patch_rates,  &sum_rates_by_row);

    return SUCCESS;
}



static void single_test_free(patch_t** world, size_t** nb_indices, double** patch_rates, double** sum_rates_by_row) {
    free(*world);
    free(*nb_indices);
    free(*patch_rates);
    free(*sum_rates_by_row);
    *world = NULL;
    *nb_indices = NULL;
    *patch_rates = NULL;
    *sum_rates_by_row = NULL;
}



uint8_t run(model_t* restrict mod, char* message, size_t msg_len) {
    if (!mod->data_empty) {
        // this won't happen if called from python, the ``simulation.run`` caller has checked it.
        fprintf(stdout, "Error: mod has non-empty data\n");
        fflush(stdout);
        return DATA_NOT_EMPTY;
    }

    double start = clock();

    // initialize random
    if (mod->seed != -1) {
        rand_init((uint64_t) (mod->seed));
    } else {
        rand_init((uint64_t) time(NULL));
    }
    mod->data_empty = false;

    if (mod->print_pct == 0) {
        mod->print_pct = 5;  // default print_pct
    } 
    size_t print_round = 0;  // print every some round if print_pct == x * 100, set to 0 for not printing
    if (mod->print_pct >= 100) {
        print_round = mod->print_pct / 100;  // print progress every some round
        mod->print_pct = -1;  // not printing progress in single_test
    }

    size_t round = 0;

    while (round < mod->sim_time) {
        char curr_msg[100 + msg_len];  // message for current round
        strcpy(curr_msg, message);
        strcat(curr_msg, "round ");
        snprintf(curr_msg + strlen(curr_msg), sizeof(curr_msg) - strlen(curr_msg), "%zu", round);

        if ((print_round != 0) && (round % print_round == 0)) {
            // only printing the round number
            // add "!= 0" because round 0 could trigger printing
            fprintf(stdout, "\r%s", curr_msg);
            fflush(stdout);
        }

        uint8_t result = single_test(mod, curr_msg);
        
        switch (result) {
            case SUCCESS:
                round++;
                break;
            case SMALL_MAXTIME:
                // error message is handled by single_test
                return SMALL_MAXTIME;
            case SIM_OVERFLOW:
                // error message is handled by single_test
                return SIM_OVERFLOW;
            case ACCURACY_ERROR:
                // error message is handled by single_test
                return ACCURACY_ERROR;
        }
    }

    calculate_ave(mod);

    if ((mod->print_pct != -1) || (print_round != 0)) {
        // print runtime if the original mod->print_pct != -1
        double stop = clock();
        fprintf(stdout, "\r%sruntime: %.3fs             \n", message, (double)(stop - start) / CLOCKS_PER_SEC);
        fflush(stdout);
    }
    return SUCCESS;
}



