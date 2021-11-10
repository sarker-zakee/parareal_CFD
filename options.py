import os

number_time_slice = 10
min_number_times_per_timestep = 5

start_time = 0
end_time = 50

dt_coarse = 0.02
dt_fine  = 0.02


program_rootpath = os.getcwd()
src_case_coarse = program_rootpath + "/openFoam_coarse" 
src_case_fine = program_rootpath + "/openFoam_fine"

dir_iteration = "K_"

dir_timeslice = "TS_" 


L2_norm_tolarance = 0.001