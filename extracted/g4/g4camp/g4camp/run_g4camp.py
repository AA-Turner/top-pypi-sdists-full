from g4camp.g4camp import g4camp
import time
import numpy as np
import h5py
import sys
import configargparse
import logging

log = logging.getLogger('run_g4camp')
logformat='[%(name)12s ] %(levelname)8s: %(message)s'
logging.basicConfig(format=logformat)

def report_timing(func):
    def func_wrapper(*args, **kwargs):
        tic = time.time()
        result = func(*args, **kwargs)
        toc = time.time()
        dt = toc - tic
        log .info(f'{func.__name__}'.ljust(40)+f'{dt:6.3f} seconds'.rjust(30))
        return result
    return func_wrapper


def parse_arguments():
    p = configargparse.get_argument_parser()
    p.add_argument('-n', type=int, default=2, help="number of events")
    p.add_argument('-o', type=str, default='output.h5', help="output file name")
    p.add_argument('--physics', type=str, default='Custom', help="choose physics list", choices=('Custom', 'FTFP_BERT', 'QGSP_BERT', 'QGSP_BIC'))
    p.add_argument('--mode_custom_physlist', type=str, choices=('all_phys', 'em_cascade', 'fast'), default='all_phys', help="choose available physics set")
    p.add_argument('--enable_optics', action='store_true', help="enable optics")
    p.add_argument('-p', '--primary-generator', type=str, choices=('gun','gps'), default='gun', help="type of primary generator type")
    p.add_argument('--gun_particle', type=str, default='mu-', help="gun particle type, e.g. e-, e+, gamma, mu-, pi0 etc.")
    p.add_argument('--gun_energy_GeV', type=float, default=100., help="gun particle energy in GeV")
    p.add_argument('--gun_position_m', type=float, nargs=3, default=[0.,0.,0.], help="gun position in meters")
    p.add_argument('--gun_direction', type=float, nargs=3, default=[0.,0.,1.], help="gun direction X, Y, Z components")
    p.add_argument('--gps_macro', type=str, default='muons.mac', help="macro files with Geant4 GPS commands to congigure particle source")
    p.add_argument('--event_max_energy_GeV', type=float, default=100., help="maximum energy of particles in an event in GeV")
    p.add_argument('--e_min_energy_GeV', type=float, default=1e-7, help="minimum energy of electrons/positrons in GeV")
    p.add_argument('--muhad_min_energy_GeV', type=float, default=1e-7, help="minimum energy of muons/hadrons in GeV")
    p.add_argument('--step_function_m', type=float, nargs=2, default = (0.2, 1e-4), help='Step function parameters (the second parameter is specified in meters)')
    p.add_argument('--skip_mode', type=str, choices=('cut','fraction'), default='cut', help='choice of the option for cutting secondary particles: (i) cut - through absolute values, (ii) fraction - through the fraction of the energy of the initial particle')
    p.add_argument('--skip_min', type=float, default=0.002, help="minimal of particle energy to skip")
    p.add_argument('--skip_max', type=float, default=0.01, help="maximal of particle energy to skip")
    p.add_argument('--ene_lower_edge', type=float, default=0., help="minimum total energy of the particles in the simulation")
    p.add_argument('--random_seed', type=int, default=1, help="random seed")
    p.add_argument('--photon_suppression', type=int, default=10, help="photon suppression factor")
    p.add_argument('--refractive_index', type=float, default=1.34, help="refractive index of a transparent medium")
    p.add_argument('--det_height', type=float, default=1500., help="(cylindrical) detector volume height (in meters)")
    p.add_argument('--det_radius', type=float, default=1500., help="(cylindrical) detector volume radius (in meters)")
    p.add_argument('--save_process_name', action='store_true', help='')
    p.add_argument('-l', '--log-level', type=str, choices=('deepdebug', 'debug', 'info', 'warning', 'error', 'critical'), default='info', help='logging level')

    opts = p.parse_args()
    #
    log.setLevel(opts.log_level.upper())
    log.info("----------")
    log.info(p.format_help())
    log.info("----------")
    log.info(p.format_values())    # useful for logging where different settings came from
    return opts


@report_timing
def run(app, n_events=10, ofname="output.h5"):
    h5file = h5py.File(ofname, "w")  # create empty file
    h5file.close()
    for ievt, data in enumerate(app.run(n_events)):
        h5file = h5py.File(ofname, "a")
        g = h5file.create_group(f"event_{ievt}")
        g.create_dataset('particles', data=data.particles.get_named_data())
        g.create_dataset('photons', data=data.photons.get_named_data())
        g.create_dataset('tracks', data=data.tracks.get_named_data())
        h5file.close()
        #log.info(f" Event #{ievt}/{n_events}")
        log.info(f"   Number of particles:    {data.particles.unique_data}")
        log.info(f"   Number of tracks:       {data.tracks.unique_data}")
#        log.info(f"   Number of track points: {len(data.tracks.quantities['uid'].value)}")
        log.info(f"   Number of photons:      {data.photons.unique_data}")
        db = app.data_buffer
        #log.info(f"   Number of particles / tracks points / photons : {len(db.particles):6.0f} / {len(db.tracks):6.0f} / {len(db.photons):6.0f}")
        log.info(" ")


def main():
    opts = parse_arguments()
    physics = opts.physics
    mode_physlist = opts.mode_custom_physlist
    optics = opts.enable_optics
    #
    if opts.primary_generator == 'gun':
        gun_args = {'particle': opts.gun_particle, 
                    'energy_GeV': opts.gun_energy_GeV, 
                    'position_m': opts.gun_position_m,
                    'direction': opts.gun_direction}
        app = g4camp(physics=physics, mode_physlist=mode_physlist, optics=optics, primary_generator='gun', gun_args=gun_args)
    elif opts.primary_generator == 'gps':
        app = g4camp(physics=physics, mode_physlist=mode_physlist, optics=optics, primary_generator='gps')
        app.setGPSMacro(opts.gps_macro)
    else:
        log.error(f"Wrong primary type '{opts.primary_generator}'")
    app.log = log
    app.setRandomSeed(int(opts.random_seed))
    app.setSkipMinMax(opts.skip_mode, opts.skip_min, opts.skip_max)
    app.setPhotonSuppressionFactor(opts.photon_suppression)
    app.setDetectorHeight(opts.det_height)
    app.setDetectorRadius(opts.det_radius)
    app.SaveProcessName(opts.save_process_name)
    app.configure()
    run(app, n_events=int(opts.n), ofname=opts.o)
    log.info("All done!")


if __name__ == "__main__":
    main()

