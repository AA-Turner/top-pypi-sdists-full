#! /usr/bin/env python
#
# 20190111

#  GOAL
#    Given arguments specifying the type of study, and a candidate, perform all steps needed to setup and submit the rapidpe dag job for that candidate
#     - Code should work for rapidPE studies done by both RIT and UWM
#     - Code should be able to run studies for many injections, via a wrapper script which gathers the candidate info
#     - Code will be extended to be triggered by a graceDB event/superevent
#     - Future plans: generate posterior distributions. This will be done in a separate script, but can be triggered by this script. 
#    Input: config file describing the study you want to do, and command line arguments specifying the candidate information. Candidate info can also be specified in the config file
#    User must provide arglists for both ILE and fitting/iteration jobs
#    Assumes user has done all necessary setup (e.g., PSDs, data selection, picking channel names, etc)
#    Will add in fit assessment jobs later
#
# Code base: https://git.ligo.org/sinead.walsh/automated_rapidpe_submission
# (started from https://git.ligo.org/richard-oshaughnessy/research-projects-RIT/blob/temp-RIT-Tides/MonteCarloMarginalizeCode/Code/create_event_parameter_pipeline_BasicIteration)
#
#    **NOTE** See ini_files/Example1.ini for sample input and also in-depth descriptions of much of the input ********
#
#    WORKFLOW
#        - generate initial grid
#        - optional: read bayestar skymap
#        - begin constructing dag job with multiple iterations and refined gridding after each step
#
#    OUTPUT STRUCTURE
#          output_directory identifies study/
#               subdirectory for this candidate
#                          separate sub-directory containing input and output for each iteration
#          TBD: also these?
#              - output-ILE-<iteration>.xml.gz, starting with iteration 0 (=input)
#              - *.composite files, from each consolidation step
#              - all.net : union of all *.composite files 
#   
# EXAMPLES
#    python create_event_parameter_pipeline_BasicIteration.py ini_files/Example1.ini
#    python create_event_parameter_pipeline_BasicIteration.py ini_files/Example  {<dict with event_info>}

__author__ = "Caitlin Rose, Daniel Wysocki, Sinead Walsh, Vinaya Valsan"

import sys,os,json,shlex,ast
import subprocess,time
import numpy as np

from rapid_pe import dagutils

from rapidpe_rift_pipe.modules import *

from glue import pipeline # https://github.com/lscsoft/lalsuite-archive/blob/5a47239a877032e93b1ca34445640360d6c3c990/glue/glue/pipeline.py


def main(config, event_info=None):
    cfgname = config.config_fname

    username = os.environ["USER"] ## NOTE: should allow override from config file

    exe_generate_initial_grid = "" ## TODO: one remaining holdout for switching to config.py
    if config.event_params_in_cfg:
        event_info = config.common_event_info
        #if the inital grid is not provided, it will be generated automatically within this code
    #    if ("initial_grid_xml" not in event_info) and config.exe_generate_initial_grid == "":
        if config.exe_generate_initial_grid is not None and "initial_grid_xml" not in event_info:
            exe_generate_initial_grid = config.exe_generate_initial_grid
            sys.exit("ERROR: if the initial_grid_xml is not provided, you need to provide the executable to generate the inital grid")
    elif event_info is None:
        raise ValueError(
            "Need to pass dict of event args if event not in config."
        )

    event_info["dag_script_start_time"] = time.time()

    output_dir =  event_info['output_dir']

    getenv_value = dagutils.format_getenv(config.getenv)
    environment_value = dagutils.format_environment(config.environment)

    common_condor_commands = {}

    if len(config.getenv) != 0:
        getenv_value = dagutils.format_getenv(config.getenv)
        getenv_str = f"getenv = {getenv_value}\n"
        common_condor_commands["getenv"] = getenv_value
    else:
        getenv_str = ""

    if len(config.environment) != 0:
        environment_value = dagutils.format_environment(config.environment)
        environment_str = f"environment = {environment_value}\n"
        common_condor_commands["environment"] = environment_value
    else:
        environment_str = ""

    #
    # Create new working directory for the event
    #
    print(("The directory for this event is",output_dir))
    print ("The working dir will change to the above after initial grid generation, if generating the initial grid")
#    if not os.path.isdir(init_directory+"/"+config.output_parent_directory):
#        os.system("mkdir "+init_directory+"/"+config.output_parent_directory)
    if not os.path.isdir(output_dir):
        os.system("mkdir -p "+output_dir)
    elif not config.overwrite_existing_event_dag:
        sys.exit("ERROR: event directory already exists")
    log_dir = os.path.join(output_dir,"logs","")
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
        os.mkdir(os.path.join(output_dir,"results"))
        os.mkdir(os.path.join(output_dir,"summary"))
    if config.web_dir:
        summarypage_dir = config.web_dir
    else:
        summarypage_dir = os.path.join(os.getenv("HOME"),"public_html/RapidPE/"+output_dir[output_dir.rfind("output/")+7:])
    os.makedirs(summarypage_dir, exist_ok=True)
    os.system("cp "+cfgname+" "+os.path.join(output_dir,"Config.ini"))
    os.system('echo "\n#Original config name: '+cfgname+'" >> '+os.path.join(output_dir,'Config.ini'))

    integrate_likelihood_cmds_dict = config.integrate_likelihood_cmds_dict.copy()
    if 'manual-logarithm-offset' in integrate_likelihood_cmds_dict:
        integrate_likelihood_cmds_dict["manual-logarithm-offset"] = 0.5*event_info["snr"]**2.
    if 'pipeline' in event_info and event_info['pipeline'] == 'pycbc':
        integrate_likelihood_cmds_dict['fmin-template'] = max(float(integrate_likelihood_cmds_dict['fmin-template']),float(event_info['psd_f0']))
    if "event-time" in integrate_likelihood_cmds_dict or "psd-file" in integrate_likelihood_cmds_dict or "channel-name" in integrate_likelihood_cmds_dict:
        sys.exit("ERROR: event specific info specified in LikelihoodIntegration of config and in command line or Event section of config. event_time, psd_file,cache_file and channel_name must be specified in the [Event] section or in the input event dictionary ")
    else:
        integrate_likelihood_cmds_dict["event-time"] = event_info["event_time"]
        integrate_likelihood_cmds_dict["psd-file"] = event_info["psd_file"]
        integrate_likelihood_cmds_dict["channel-name"] = event_info["channel_name"]
        integrate_likelihood_cmds_dict["cache-file"] = event_info["cache_file"]
        integrate_likelihood_cmds_dict["approximant"] = event_info["approximant"]
        if "data_start_time" in event_info:
            integrate_likelihood_cmds_dict["data-start-time"] = event_info["data_start_time"]
            integrate_likelihood_cmds_dict["data-end-time"] = event_info["data_end_time"]
        if "skymap_file" in event_info:
            integrate_likelihood_cmds_dict["skymap-file"] = event_info["skymap_file"]

    if config.submit_only_at_exact_signal_position:
        #This is the filename for the output at each intrinsic grid point
        integration_output_file_name = os.path.join(output_dir,"results/ILE_iteration_exact_intrinsic")
        if 'injection_param' in event_info:
            inj_param = convert_list_string_to_dict(event_info["injection_param"])
        else:
            inj_param = convert_list_string_to_dict(event_info["intrinsic_param"])

        newlines = "universe = vanilla\n"
        newlines += "executable = "+sys.executable+"\n"
        #newlines += "executable = "+config.exe_integration_extrinsic_likelihood+"\n"
       # newlines += 'arguments = " '
        if config.cProfile:
            newlines += f"arguments = \" -m cProfile -o {log_dir}/cprofile_integrate.out " + config.exe_integration_extrinsic_likelihood
        else:
            newlines += "arguments = \" "+ config.exe_integration_extrinsic_likelihood
        newlines += " --output-file="+integration_output_file_name
        newlines += " --mass1 "+str(inj_param["mass1"])+" --mass2 "+str(inj_param["mass2"])
        if 'spin1z' in inj_param:
            newlines += " --spin1z "+str(inj_param["spin1z"])+" --spin2z "+str(inj_param["spin2z"])
        newlines += " "+convert_dict_to_cmd_line(integrate_likelihood_cmds_dict)
        newlines += ' "\n'
        newlines += "request_memory = 2048\n"
        newlines += "accounting_group = "+config.accounting_group+"\n"
        newlines += "accounting_group_user = "+config.accounting_group_user+"\n"
        newlines += getenv_str
        newlines += environment_str
        newlines += "request_disk = 512\n"
        newlines += f"log = {log_dir}/integrate.log\nerror = {log_dir}/integrate.err\noutput = {log_dir}/integrate.out\n"
        newlines += "notification = never\nqueue 1\n"

        for k, v in config.integrate_likelihood_condor_commands.items():
            newlines += f"{k} = {v}"

        sub_file_path = os.path.join(output_dir,"integrate.sub")
        with open(sub_file_path,"w") as fo:
            fo.write(newlines)

        event_info["condor_submit_time"] = time.time()
        #Write the event_info dictionary to the output dir
        with open(os.path.join(output_dir,"event_info_dict.txt"),"w") as ef:
            ef.write(json.dumps(event_info))

        print("Job ready for submission",sub_file_path)
        if config.submit_dag:
            os.system("condor_submit "+sub_file_path)
        return
    else:
        #If you have specified an executable to generate the initial intrinsic grid, it is run here. It must return the initial_grid_xml name
        if exe_generate_initial_grid != "":
            print ("Generate initial grid")
            stdout_grid_gen = subprocess.Popen(exe_generate_initial_grid+" "+cfgname+" | grep 'initial_grid_xml='",stdout=subprocess.PIPE,shell=True).communicate()[0]
            if not "initial_grid_xml" in stdout_grid_gen:
                sys.exit("ERROR: grid generator must return output xml filename in format [initial_grid_xml=filename]")

            stdout_dict = convert_list_string_to_dict(stdout_grid_gen)
            event_info["initial_grid_xml"] = stdout_dict["initial_grid_xml"]
            if "initial_grid_hdf" in stdout_dict:
                event_info["initial_grid_hdf"] = stdout_dict["initial_grid_hdf"]


        #if initial grid isn't local, or doesn't hvae the iteration_0 identifier, copy to event dir and append iteration_0
        intrinsic_grid_xml = (event_info["initial_grid_xml"][event_info["initial_grid_xml"].rfind("/")+1:])
        if not "iteration_0" in intrinsic_grid_xml:
            #FIXME: want to remove path info from event_info["initial_grid_xml"] before this copy
            intrinsic_grid_xml = intrinsic_grid_xml[intrinsic_grid_xml.rfine("/")+1:] if "/" in intrinsic_grid_xml else intrinsic_grid_xml
            intrinsic_grid_xml = intrinsic_grid_xml.replace(".xml.gz","iteration_0.xml.gz")
            os.system("cp "+event_info["initial_grid_xml"]+" "+os.path.join(output_dir,intrinsic_grid_xml))
        else:
            os.system("cp "+event_info["initial_grid_xml"]+" "+os.path.join(output_dir,""))

        print(("Intrinsic grid for iteration 0",intrinsic_grid_xml))

        ###
        ### With the inital grid generated, you have all the information you need to run iteration 0. You set up the dag for that here, using rapidpe_create_event_dag in lalsuite. FIXME: this only works for m1 m2. It needs to be adapted for any dimension by taking 
        ### The output .dag file has a few lines for every m1 m2 etc point with the values of the point. The output .sh file has the values filled into the common command line arguements for integrate extrinsic likelihood. The only variable that remains to be filled in the integarte commands is the name of the output file, which includes the cluster and process id. Why are these neeed? I don't know, but it's probably for debugging
        ###
        ### output-name is the name of the dag files for iteration 0. output-file is the name of the file output per intrinsic grid point. The latter will have the massID, cluster and process appended to it.
        ###
        ### FIXME: What doesn the output xml.gz file contain. output name and output file are independent
 
        #event specific commands which need to be lassed to the integration exe are added to the dict here
        #This is the filename for the output at each intrinsic grid point
        integration_output_file_base = os.path.join(output_dir,"results/ILE_iteration_")
#        integrate_likelihood_cmds_dict["output-file"] = integration_output_file_base+"0.xml.gz"
        iteration_dag_name = os.path.join(output_dir,"marginalize_extrinsic_parameters_iteration_0")

        print ("Constructing iteration 0 event dag with command lines for each intrinsic grid point")
        #FIXME: the condor-command option is the condor_commands for the integration. should be possible to pass via LikelihoodIntegration cmd. 
        #accounting_group is passed by default because it's required for all jobs.
        it_0_dag_cmd = config.exe_create_event_dag + " --condor-command accounting_group="+config.accounting_group+" --accounting-group-user "+config.accounting_group_user+" --exe-integrate-likelihood "+config.exe_integration_extrinsic_likelihood+" --working-directory "+ output_dir+ " --log-directory "+log_dir+" --integration-args-dict='"+json.dumps(integrate_likelihood_cmds_dict, sort_keys=True)+"' --write-script "
        if config.cProfile:
            it_0_dag_cmd += " --cProfile"
        #Variables which change per iteration are difined below 
        it_0_dag_cmd +=" --output-name "+iteration_dag_name+" --template-bank-xml "+os.path.join(output_dir,intrinsic_grid_xml)
        #event time is within the integrate_likelihood_cmds_dict but it's also defined here because it's used within create_event_dag, not just passed to the integrate exe
        it_0_dag_cmd +=" --event-time="+event_info["event_time"]
        #This is only used by the likelihood itegration exe, but it changes per iteration so it is defined here, which means that any exe used has to 
        #take --output-file as an argumnet
        it_0_dag_cmd +=" --output-file "+integration_output_file_base+"0.xml.gz"
        it_0_dag_cmd += " --iteration-level 0"
        # Pass getenv and environment variables if set
        if len(config.getenv) != 0:
            it_0_dag_cmd += f" --getenv {' '.join(config.getenv)}"
        if len(config.environment) != 0:
            environment_json = json.dumps(config.environment)
            environment_quoted = shlex.quote(environment_json)
            it_0_dag_cmd += f" --environment {environment_quoted}"
        #You can pass extra create_event_dag options by creating a section called CreateEventDag and adding them there.
        ## TODO: integrate into config.py
        it_0_dag_cmd += convert_dict_to_cmd_line(config.create_event_dag_info)

        for k, v in config.integrate_likelihood_condor_commands.items():
            it_0_dag_cmd += f" --condor-command {k}={v}"

        print(("Iteration 0 dag cmd:\n",  it_0_dag_cmd))
        exit_status = os.system(it_0_dag_cmd)
        if exit_status != 0:
            print(it_0_dag_cmd)
            sys.exit("ERROR: non zero exit status "+str(exit_status))

        print ("Iteration 0 dag construction complete")

        ###
        ### DAG generation
        ### I don't see the benefit of using the dagutils or dag_utils functions which then use the glue.pipeline functions to write the dag. So I write the dag here instead
        ###

        print ("Constructing uberdag")
        #this is a hold-all container for all subdags, doesn't appear to correspond to and specific file
        uberdag = pipeline.CondorDAG(log=output_dir)
        event_dag_name = os.path.join(output_dir,"event_all_iterations")
        uberdag.set_dag_file(event_dag_name)

        # This is meant to ensure that the DAG continues even if some of the integrator jobs fail                                        
        # It also prints the time that the job completed
        passthrough_filename = os.path.join(output_dir,"passthrough_%ITER%.sh")
        passthrough_str = f"#!/bin/bash\necho %ITER% `date +%s` >> {output_dir}/job_timing.txt\n/bin/true"
        indx = 0
        iter_pt_filename = passthrough_filename.replace("%ITER%",str(int(indx)))
        iter_pt_str =passthrough_str.replace("%ITER%",str(int(indx)))
        with open(iter_pt_filename, "w") as fout:
            print(iter_pt_str, file=fout)
        os.chmod(iter_pt_filename, 0o744)

        #This is the dag for iteration 0
        subdag = pipeline.CondorDAGManJob(iteration_dag_name + ".dag")
        analysis_node = subdag.create_node()
        analysis_node.set_post_script(iter_pt_filename)
        uberdag.add_node(analysis_node)

        print ("Passthrough script added")

        print ("Generating gridding sub file")
        #After iteration 0, you need to run rapidpe_compute_intrinsic_grid to get the intrinsic grid for the next stage.
        grid_refine_kwargs = config.grid_refine_info
        if config.use_event_spin:
            event_spin = event_info["event_spin"]
            grid_refine_kwargs['pin-param'] = [f"spin1z={event_spin['spin1z']}",f"spin2z={event_spin['spin2z']}"]
        grid_job = write_generic_dag_job(config.exe_grid_refine, "GridRefine", output_dir, config.accounting_group,config.accounting_group_user, grid_refine_kwargs, config.grid_refine_condor_commands | common_condor_commands)
        #### These options may only apply for the lalsuite rapidpe_compute_intrinsic_grid. If we want to use a different grid refinement scheme we'll need to add a switch here.
        #It requires a .hdf file, which has the grid information for each preceding level. This file is generated by rapidpe_compute_intrinsic_grid when generating the initial grid.
        grid_job.add_opt("refine",event_info["initial_grid_hdf"])
        grid_job.add_opt("output-xml-file-name",os.path.join(output_dir,"$(macrooutputxmlfilename)"))
        #take the output from all previous iterations to calculate the confidence region. Since this ready *.xml.gz, it is reading the results from all previous stages. So the command line doesn't change per iteration but the input will be different as it is run after each iteration.
        grid_job.add_opt("result-file","'"+integration_output_file_base+"*.xml.gz'")
        grid_job.write_sub_file()
        print ("Gridding sub file complete")

        #This is the dag for rapidpe_create_event_dag. This creates the  marginalize_extrinsic_parameters_iteration_N.dag in the same way as done for iteration 0 above.
        iteration_job = write_generic_dag_job(config.exe_create_event_dag, "CreateEventDag",output_dir, config.accounting_group, config.accounting_group_user,config.create_event_dag_info, config.create_event_dag_condor_commands | common_condor_commands)
        #Option added to create_event_dag to use integration.sub file which was generated for iteration 0, regenerating it is unnecessary.
        #FIXME: add this option to rapidpe_create_event_dag
        iteration_job.add_opt("condor-command","accounting_group="+config.accounting_group)
        # HACK: glue.pipeline doesn't allow repeated add_opt calls with the same
        #       key, because it uses a dict to store them.  Using add_arg
        #       instead to append additional --condor-command options.
        for k, v in config.integrate_likelihood_condor_commands.items():
            iteration_job.add_arg(f"--condor-command {k}={v}")
        iteration_job.add_opt("accounting-group-user",config.accounting_group_user)
        if len(config.getenv) != 0:
            iteration_job.add_opt("getenv", " ".join(config.getenv))
        if len(config.environment) != 0:
            iteration_job.add_opt(
                "environment",
                shlex.quote(json.dumps(config.environment)).replace('"', '""'))
        iteration_job.add_opt("working-directory",output_dir)
        # Name / tag for the output of the per intrinsic grid point integration
        iteration_job.add_opt("output-file", "$(macrooutputfile)")
        iteration_job.add_opt("iteration-level", "$(iterlevel)")
        # Name / tag for DAG itself, which runs the integration for all intrinsic grid points
        iteration_job.add_opt("output-name", "$(macrooutputname)")
        # Input grid points to generate the margianlization jobs
        iteration_job.add_opt("template-bank-xml", os.path.join(output_dir,"$(macroinputname)"))
        #same as for iteration 0, this is the stuff needed to run the integration per intrinsic grid point. and some default stuff 
        iteration_job.add_opt("exe-integrate-likelihood", config.exe_integration_extrinsic_likelihood)
        iteration_job.add_opt("log-directory", log_dir)
#        iteration_job.add_opt("integration-args-dict", "'"+json.dumps(integrate_likelihood_cmds_dict, sort_keys=True).replace('"','\\"')+"'")
        #Condor dag jobs require a very strange very specific format for string submission. see http://research.cs.wisc.edu/htcondor/manual/v7.6/2_10DAGMan_Applications.html. In short the dict string needs to be passed as '{""a"": ""0"",""b"": ""[\""var1\""]""}'
        iteration_job.add_opt("integration-args-dict", "'"+(json.dumps(integrate_likelihood_cmds_dict, sort_keys=True).replace('"','""'))+"'")
#        tmp_test = "\"\"{\'n-max\': \'10000\'}\"\""
#        iteration_job.add_opt("integration-args-dict", tmp_test)
        iteration_job.add_opt("event-time", event_info["event_time"])
        iteration_job.add_opt("write-script", "")
        if config.cProfile:
            iteration_job.add_opt("cProfile", "")
        iteration_job.write_sub_file()
        print ("Create event dag subfile complete")

        #This assignment is for naming consistency
        #FIXME: currently disabled option to begin iterating at an input iteraton. Should reimplement this, make sure overwite_dag=1 if start iteration is set. check results from previous step exist, read in those
        for indx in np.arange(1,config.n_iterations_per_job):
#            iteration_dir = output_dir+"/iteration_"+str(indx)
#            os.mkdir(iteration_dir); os.mkdir(iteration_dir+"/logs")
            print(("Level ",indx))

            #Set the names of input and output files for create event dag 
            integration_output_file = integration_output_file_base+str(indx)+".xml.gz"
            iteration_dag_name = iteration_dag_name.replace("iteration_%d" % (indx-1), "iteration_%d" % indx)
            #WARNING: If using rapidpe_compute_intrinsic_grid the iteration/level is determined internally from the hdf file. The output file name is hardcoded, so we cant change it here.        
            intrinsic_grid_xml = intrinsic_grid_xml.replace("LEVEL_%d" % (indx-1), "LEVEL_%d" % indx) if "LEVEL" in intrinsic_grid_xml else intrinsic_grid_xml.replace("iteration_%d" % (indx-1), "iteration_%d" % indx)


            #
            ### Create the gridding job which will generate the intrinsic grid for iteration n based of the results of iteration n-1
            #
            #With rapidpe_compute_intrinsic_grid: Note, the name of the output xml file containing the level n grid is automatic. "HL-MASS_POINTS_LEVEL_%d-0-1.xml.gz" % level. Also, the level is determined automatically from the hdf file. The generated grid is appended to the hdf file.
            grid_job_node = pipeline.CondorDAGNode(grid_job)
            #In this implementation, the .sub file has no variables because the output of all previous stages are read
#            grid_job_node.add_macro("macroresultfile", result_file)
            #This adds the level n gridding node to the CondorDAG object
            uberdag.add_node(grid_job_node)
            grid_job_node.add_macro("macrooutputxmlfilename",intrinsic_grid_xml)
            #This sets the CondorDAGManJob as the parent
            grid_job_node.add_parent(analysis_node)


            #
            ### Create the iteration N dag job which will generate the integration command line for each intrinsic grid point from the gridding job
            #
            iteration_job_node = pipeline.CondorDAGNode(iteration_job)
            iteration_job_node.add_macro("macrooutputname", iteration_dag_name)
            iteration_job_node.add_macro("macrooutputfile",integration_output_file)
            iteration_job_node.add_macro("macroinputname", intrinsic_grid_xml)
            iteration_job_node.add_macro("iterlevel", str(indx))
            uberdag.add_node(iteration_job_node)
            iteration_job_node.add_parent(grid_job_node)

            # This is the proxy for the iteration SUBDAG that hasn't been created yet --- that's                                                         
            # okay, condor never checks until execution that it even exists. This is                                                                               
            # here so that parent and child nodes have something to reference                                                                                      
            subdag = pipeline.CondorDAGManJob(iteration_dag_name + ".dag")
            analysis_node = subdag.create_node()

            iter_pt_filename = passthrough_filename.replace("%ITER%",str(int(indx)))
            #If it's the last command, it should launch the plotting script
            #FIXME: should this be optional?
            iter_pt_str = passthrough_str.replace("%ITER%",str(int(indx)))
            web_dir_str = ""
            if config.web_dir:
                web_dir_str = f"--web-dir {config.web_dir}"
            summary_plots_outfile = os.path.join(output_dir,"summary/summary_plots.out")
            if indx == (config.n_iterations_per_job-1):
                iter_pt_str = f"#!/bin/bash\necho {str(int(indx))} `date +%s` >> {output_dir}/job_timing.txt\n"
                iter_pt_str += f"echo 'job_complete' >> {output_dir}/JOB_COMPLETE\n"
                seed_arg = f'--seed {config.seed}' if config.seed is not None else ''
                iter_pt_str += f"compute_posterior.py {output_dir} --distance-coordinates {config.distance_coordinates} {seed_arg} &>> {summary_plots_outfile}\n"
                if config.cProfile:
                    iter_pt_str += f"cprofile_summary.py {output_dir} &>> {summary_plots_outfile}\n"
                iter_pt_str += f"create_summarypage.py {output_dir} {web_dir_str}  &>> {summary_plots_outfile}\n"
                #automatically plot the posteriors when the job is done. FIXME: change 0.99 to whatever
                #iter_pt_str += "python "+init_directory+"/plot_all_posteriors.py "+output_dir+" 0.99\n"
                #iter_pt_str += "python "+init_directory+"/plot_all_posteriors.py "+output_dir+" 0.9\n"
                #iter_pt_str += "python "+init_directory+"/plot_all_posteriors_vinaya.py "+output_dir+" 0\n"
                if config.email_address_for_job_complete_notice != "":
                    iter_pt_str += "echo 'Job complete, see https://ldas-jobs.ligo.caltech.edu/~"+username+"/RapidPE/"+output_dir[output_dir.rfind("output/")+7:]+"' | mail -s 'rapidPE:"+config.output_parent_directory+"' "+config.email_address_for_job_complete_notice+"\n"
                iter_pt_str += "/bin/true"        
            with open(iter_pt_filename, "w") as fout:
                print(iter_pt_str, file=fout)
            os.chmod(iter_pt_filename, 0o744)

            analysis_node.set_post_script(iter_pt_filename)
            uberdag.add_node(analysis_node)
            analysis_node.add_parent(iteration_job_node)


        uberdag.write_concrete_dag()
        uberdag.write_script()

        event_info["condor_submit_time"] = time.time()
        #Write the event_info dictionary to the output dir
        with open(os.path.join(output_dir,"event_info_dict.txt"),"w") as ef:
            ef.write(json.dumps(event_info, sort_keys=True))

        if config.submit_dag:
            print("Submitting DAG", event_dag_name)

            args = ["condor_submit_dag"]

            # Need to pass any variables named in config.getenv
            if len(config.getenv) != 0:
                args += ["-include_env", ",".join(config.getenv)]

            args.append(f"{event_dag_name}.dag")

            subprocess.run(args)


##%##   Consolidate job(s)
##%#   - consolidate output of single previous job
##%con_job, con_job_name = dag_utils.write_consolidate_sub_simple(tag='join',log_dir=None,arg_str='',base=opts.working_directory+"/iteration_$(macroiteration)_ile", target=opts.working_directory+'/consolidated_$(macroiteration)')
##%# Modify: set 'initialdir' : should run in top-level direcory
##%#con_job.add_condor_cmd("initialdir",opts.working_directory+"/iteration_$(macroiteration)_con")
##%# Modify output argument: change logs and working directory to be subdirectory for the run
##%con_job.set_log_file(opts.working_directory+"/iteration_$(macroiteration)_con/logs/con-$(cluster)-$(process).log")
##%con_job.set_stderr_file(opts.working_directory+"/iteration_$(macroiteration)_con/logs/con-$(cluster)-$(process).err")
##%con_job.set_stdout_file(opts.working_directory+"/iteration_$(macroiteration)_con/logs/con-$(cluster)-$(process).out")
##%con_job.write_sub_file()
##%
##%##   Unify job
##%#   - update 'all.net' to include all previous events
##%unify_job, unify_job_name = dag_utils.write_unify_sub_simple(tag='unify',log_dir='',arg_str='', base=opts.working_directory, target=opts.working_directory+'/all.net')
##%unify_job.add_condor_cmd("initialdir",opts.working_directory)
##%unify_job.set_log_file(opts.working_directory+"/iteration_$(macroiteration)_con/logs/unify-$(cluster)-$(process).log")
##%unify_job.set_stderr_file(opts.working_directory+"/iteration_$(macroiteration)_con/logs/unify-$(cluster)-$(process).err")
##%unify_job.set_stdout_file(opts.working_directory+"/all.net")
##%unify_job.write_sub_file()
##%
##%##   Fit job
##%cip_job, cip_job_name = dag_utils.write_CIP_sub(tag='CIP',log_dir=None,arg_str=cip_args,request_memory=opts.request_memory_CIP,input_net=opts.working_directory+'/all.net',output='overlap-grid-$(macroiterationnext)',out_dir=opts.working_directory,exe=opts.cip_exe)
##%# Modify: set 'initialdir'
##%cip_job.add_condor_cmd("initialdir",opts.working_directory+"/iteration_$(macroiteration)_cip")
##%# Modify output argument: change logs and working directory to be subdirectory for the run
##%cip_job.set_log_file(opts.working_directory+"/iteration_$(macroiteration)_cip/logs/cip-$(cluster)-$(process).log")
##%cip_job.set_stderr_file(opts.working_directory+"/iteration_$(macroiteration)_cip/logs/cip-$(cluster)-$(process).err")
##%cip_job.set_stdout_file(opts.working_directory+"/iteration_$(macroiteration)_cip/logs/cip-$(cluster)-$(process).out")
##%cip_job.write_sub_file()



def write_generic_dag_job(exe, job_name,output_dir, accounting_group,accounting_group_user, dict_of_kwargs,dict_of_condor_commands={},log_dir="logs/",log_files_uniq_str = "$(cluster)-$(process)"):
    ###
    ### Utility function to construct a generic condor job for the top level hierarchy of the DAG.
    ### given an executable, and a config section with command line arguments which can be read directly and do not change from dag node to node, create a generic dag job
    ### This returns the dag job object, so variable arguments can be added later
    ### the job_name is used for the sub file and to identify log files
    ###

    dag_job = pipeline.CondorDAGJob(universe="vanilla", executable=exe)
    dag_job.set_sub_file(os.path.join(output_dir,f"{job_name}.sub"))

    #
    # Logging options
    #
    log_dir = os.path.join(output_dir,log_dir)
    dag_job.set_log_file("%s%s-%s.log" % (log_dir, job_name, log_files_uniq_str))
    dag_job.set_stderr_file("%s%s-%s.err" % (log_dir, job_name, log_files_uniq_str))
    dag_job.set_stdout_file("%s%s-%s.out" % (log_dir, job_name, log_files_uniq_str))

    new_kwargs = {}
    for opt, param in dict_of_kwargs.items():
        if len(param) > 1 and param[0] == "[" and param[-1] == "]":
            param = ast.literal_eval(param)
        new_kwargs[opt.replace("_","-")] = param
    kwargs=new_kwargs


    for opt, param in kwargs.items():
        if isinstance(param, list) or isinstance(param, tuple):
            # NOTE: Hack to get around multiple instances of the same option
            for p in param:
                dag_job.add_arg("--%s %s" % (opt, str(p)))
        elif param == True or param == None:
            dag_job.add_opt(opt, '')
        # Explcitly check for False to turn it off
        elif param == False:
            continue
        else:
            dag_job.add_opt(opt, str(param))

    if 'request_memory' not in dict_of_condor_commands:
        # Memory request is 2 GB by default
        dag_job.add_condor_cmd('request_memory', '2048')
    if 'request_disk' not in dict_of_condor_commands:
        # Disk request is 512 MB by default
        dag_job.add_condor_cmd('request_disk', '512')
    dag_job.add_condor_cmd('accounting_group', accounting_group)
    dag_job.add_condor_cmd('accounting_group_user', accounting_group_user)

    # Typically used to add things like accounting information.
    for cmd, value in dict_of_condor_commands.items():
        dag_job.add_condor_cmd(cmd, value)

    # This is a hack since CondorDAGJob hides the queue property 
    dag_job._CondorJob__queue = 1
    print(("Writing sub file",job_name+".sub"))

    return dag_job



if __name__ == '__main__':
    main()
