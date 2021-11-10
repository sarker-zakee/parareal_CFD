import numpy as np
import os
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
import utility_foam as utf
import options as opt
import adjustment as adj
import shutil
import convergence as cvg



program_rootpath = os.getcwd()
src_case_coarse = program_rootpath + "/openFoam_coarse" 
src_case_fine = program_rootpath + "/openFoam_fine"

reference_fine_run = "ref_run_fine"
# setup reference_fine_run structure
utf.setup_fine(src_case_fine,reference_fine_run)
# setup time for reference_fine_run
utf.modify_control_param(reference_fine_run,{"startTime":opt.start_time,"endTime":opt.end_time})
# run reference_fine_run 
utf.run_openfoam(reference_fine_run)
# create variable to save all data
cvg.allvar_ref(reference_fine_run)

iter_counter = 0 
iter_dir = opt.dir_iteration+str(iter_counter)
init_coarse_dir = iter_dir + "/coarse"
coarse_bar_dir = iter_dir + "/coarse_bar"
fine_bar_dir   = iter_dir + "/fine_bar"
diff_timeslices = ((opt.end_time - opt.start_time)*1.0) /opt.number_time_slice

# make iteration directories
try:
    os.mkdir(iter_dir)
    print("Directory created "+ iter_dir)
except FileExistsError as fe:
    print(iter_dir + " already exist")
    pass

# make coarse dir
try:
    os.mkdir(init_coarse_dir)
    print("initial coarse directory created "+ init_coarse_dir)
except FileExistsError as fe:
    print(init_coarse_dir + " already exist")
    pass
# setup coarse structure
utf.setup_coarse(src_case_coarse,init_coarse_dir)
# setup time for coasre
utf.modify_control_param(init_coarse_dir,{"startTime":opt.start_time,"endTime":opt.end_time})
# initial coarse propagation 
utf.run_openfoam(init_coarse_dir)





# make coarse bar dir
try:
    os.mkdir(coarse_bar_dir)
    print("Directory created "+ coarse_bar_dir)
except FileExistsError as fe:
    print(coarse_bar_dir + " already exist")
    pass


ts_tpl = []
for time_slice in range(1,opt.number_time_slice+1):
    ts_dir = coarse_bar_dir+'/'+opt.dir_timeslice+str(time_slice)
    try:
         os.mkdir(ts_dir)
         print("Directory created "+ ts_dir)
    except FileExistsError as fe:
        print(ts_dir + " already exist")
        pass
    # setup coarse structure
    utf.setup_coarse(src_case_coarse,ts_dir)
    s_time = opt.start_time + diff_timeslices * (time_slice -1)
    e_time = s_time + diff_timeslices
    ts_tpl.append((int(s_time),int(e_time)))
    utf.modify_control_param(ts_dir,{"startTime":int(s_time),"endTime":int(e_time)})
    try:
        shutil.rmtree(ts_dir+"/0")
    except FileNotFoundError as fe:
        print('already deleted '+ts_dir+"/0")
    src = init_coarse_dir+'/'+str(int(s_time))
    dst = ts_dir+'/'+str(int(s_time))
    try:
        shutil.copytree(src,dst)
        print("Copying "+src+"---->"+dst)
    except FileExistsError as fe:
        print(src+"---->"+dst+" already copied")


utf.runfoam_all_timeslice(coarse_bar_dir)

# make fine bar dir 
try:
    os.mkdir(fine_bar_dir)
    print("Directory created "+ fine_bar_dir)
except FileExistsError as fe:
    print(fine_bar_dir + " already exist")
    pass


ts_tpl = []
for time_slice in range(1,opt.number_time_slice+1):
    ts_dir = fine_bar_dir+'/'+opt.dir_timeslice+str(time_slice)
    try:
         os.mkdir(ts_dir)
         print("Directory created "+ ts_dir)
    except FileExistsError as fe:
        print(ts_dir + " already exist")
        pass
    # setup coarse structure
    utf.setup_fine(src_case_fine,ts_dir)
    s_time = opt.start_time + diff_timeslices * (time_slice -1)
    e_time = s_time + diff_timeslices
    ts_tpl.append((int(s_time),int(e_time)))
    # setup time for coasre
    utf.modify_control_param(ts_dir,{"startTime":int(s_time),"endTime":int(e_time)})
    if time_slice == 1 :
        pass
    else:
        try:
            shutil.rmtree(ts_dir+"/0")
        except FileNotFoundError as fe:
            print('already deleted '+ts_dir+"/0")
        utf.run_mapfield(src="../../coarse",dst=ts_dir)




print(ts_tpl)

notconverged = True


while(notconverged):

    print("start running pisofoam parallely")
    utf.runfoam_all_timeslice(fine_bar_dir)
    cvg.allvar_iteration(fine_bar_dir)

    notconverged = cvg.convergence_check(reference_fine_run,fine_bar_dir,iter_counter)
    if notconverged:
        adj.adjust_starting_value(ts_tpl,iter_counter+1)

        iter_counter = iter_counter + 1
        iter_dir = opt.dir_iteration+str(iter_counter)
        fine_bar_dir   = iter_dir + "/fine_bar"
    else : 
        print("no change of relative error between last two iteration")
        exit()