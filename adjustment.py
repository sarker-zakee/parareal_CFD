import options as opt
import os 
import shutil
import utility_foam as utf
import jump
import projection as prj

def adjust_starting_value(ts_tpl,iteration):
    

    iter_counter = iteration
    iter_dir = opt.dir_iteration+str(iter_counter)

    prev_iter = iteration - 1
    prev_iter_dir = opt.dir_iteration+str(prev_iter)

    coarse_bar_dir = iter_dir + "/coarse_bar"
    fine_bar_dir   = iter_dir + "/fine_bar"

    diff_timeslices = ((opt.end_time - opt.start_time)*1.0) /opt.number_time_slice

    try:
        os.mkdir(iter_dir)
        print("Directory created "+ iter_dir)
    except FileExistsError as fe:
        print(iter_dir + " already exist")


    for time_slice in range(1,iteration+1):
    # for time_slice in range(1,1+1):
        from_dir = opt.dir_iteration+str(iteration-1)+'/coarse_bar/'+opt.dir_timeslice+str(time_slice)
        to_dir = coarse_bar_dir +'/'+opt.dir_timeslice+str(time_slice)
        try:
            shutil.copytree(from_dir,to_dir)
            print("Copying "+from_dir+"---->"+to_dir)
        except FileExistsError as fe:
            print(from_dir+"---->"+to_dir+" already copied")
        from_dir = opt.dir_iteration+str(iteration-1)+'/fine_bar/'+opt.dir_timeslice+str(time_slice)
        to_dir = fine_bar_dir +'/'+opt.dir_timeslice+str(time_slice)
        try:
            shutil.copytree(from_dir,to_dir)
            print("Copying "+from_dir+"---->"+to_dir)
        except FileExistsError as fe:
            print(from_dir+"---->"+to_dir+" already copied")

    for time_slice in range(iteration,opt.number_time_slice):
    # for time_slice in range(1,opt.number_time_slice):
    
        restrict_fine_bar_dir = iter_dir + "/R_fine_bar_k_"+str(prev_iter)+"_n_"+str(time_slice)
        try:
            os.mkdir(restrict_fine_bar_dir)
            print("Directory created "+ restrict_fine_bar_dir)
        except FileExistsError as fe:
            print(restrict_fine_bar_dir + " already exist")

        utf.setup_coarse(opt.src_case_coarse,restrict_fine_bar_dir)
        utf.modify_control_param(restrict_fine_bar_dir,{"startTime":ts_tpl[time_slice-1][1],"endTime":ts_tpl[time_slice-1][1]})
        try:
            shutil.rmtree(restrict_fine_bar_dir+"/0")
        except FileNotFoundError as fn:
            print(restrict_fine_bar_dir+"/0"+" alredy deleted")
        prev_fine_bar = prev_iter_dir+ "/fine_bar/"+ opt.dir_timeslice+str(time_slice)
        # interpolate, mapNearest , cellPointInterpolate
        utf.run_mapfield(src = "../../"+prev_fine_bar, dst = restrict_fine_bar_dir,mapmethod="mapNearest")
        # to prevent redo mapfield and resetup the coarse dir
        if not os.path.exists(restrict_fine_bar_dir+"/checkpoint.txt"):
            with open(restrict_fine_bar_dir + "/checkpoint.txt","w+") as ckpt:
                ckpt.write("Done"+"\n")
                ckpt.close()

    

        coarse_bar_dir_last = iter_dir + "/coarse_bar_k_" + str(prev_iter) +"_n_"+str(time_slice)
        try:
            os.mkdir(coarse_bar_dir_last)
            print("Directory created "+ coarse_bar_dir_last)
        except FileExistsError as fe:
            print(coarse_bar_dir_last + " already exist")
        utf.setup_coarse(opt.src_case_coarse,coarse_bar_dir_last)
        utf.modify_control_param(coarse_bar_dir_last,{"startTime":ts_tpl[time_slice-1][1],"endTime":ts_tpl[time_slice-1][1]})
        try:
            shutil.rmtree(coarse_bar_dir_last+"/0")
        except FileNotFoundError as fn:
            print(coarse_bar_dir_last+"/0"+" alredy deleted")
        prev_coarse_bar = prev_iter_dir+ "/coarse_bar/"+ opt.dir_timeslice+str(time_slice)
        src = prev_coarse_bar+'/'+str(ts_tpl[time_slice-1][1])
        dst = coarse_bar_dir_last +'/'+str(ts_tpl[time_slice-1][1])
        try:
            shutil.copytree(src,dst)
            print("Copying "+src+"---->"+dst)
        except FileExistsError as fe:
            print(src+"---->"+dst+" already copied")
        # to prevent redo copy and resetup the coarse dir
        if not os.path.exists(coarse_bar_dir_last+"/checkpoint.txt"):
            with open(coarse_bar_dir_last + "/checkpoint.txt","w+") as ckpt:
                ckpt.write("Done"+"\n")
                ckpt.close()


        coarse_current_dir = coarse_bar_dir +'/'+opt.dir_timeslice+str(time_slice)
        target_coarse_dir  = coarse_bar_dir +'/'+opt.dir_timeslice+str(time_slice + 1)

        utf.run_openfoam(coarse_current_dir)
        # prepare next coarse start value adjusting with jump
        jump_banner = """
 {}           {}          {}       {}
C    =  G   (C  )  +   R(F  )  -  C  
 {}      dt   {}          {}       {}
 
        """.format(time_slice,time_slice-1,time_slice,time_slice,iteration,iteration,iteration-1,iteration-1)
        print(jump_banner)
        print("["+target_coarse_dir+"] = ["+coarse_current_dir +"] + ["+restrict_fine_bar_dir+"] - ["+coarse_bar_dir_last+"]")
        jump.adjust_jump(coarse_current_dir,restrict_fine_bar_dir,coarse_bar_dir_last,ts_tpl,time_slice, target_coarse_dir)
        
        
        lifted_restrict_fine_bar_dir = iter_dir + "/L_R_fine_bar_k_"+str(prev_iter)+"_n_"+str(time_slice)
        try:
            os.mkdir(lifted_restrict_fine_bar_dir)
            print("Directory created "+ lifted_restrict_fine_bar_dir)
        except FileExistsError as fe:
            print(lifted_restrict_fine_bar_dir + " already exist")
        utf.setup_fine(opt.src_case_fine,lifted_restrict_fine_bar_dir)
        utf.modify_control_param(lifted_restrict_fine_bar_dir,{"startTime":ts_tpl[time_slice-1][1],"endTime":ts_tpl[time_slice-1][1]})
        try:
            shutil.rmtree(lifted_restrict_fine_bar_dir+"/0")
        except FileNotFoundError as fn:
            print(lifted_restrict_fine_bar_dir+"/0"+" alredy deleted")
        
        utf.run_mapfield(src="../../"+restrict_fine_bar_dir,dst=lifted_restrict_fine_bar_dir)
        # to prevent redo mapfield and resetup the fine dir
        if not os.path.exists(lifted_restrict_fine_bar_dir+"/checkpoint.txt"):
            with open(lifted_restrict_fine_bar_dir + "/checkpoint.txt","w+") as ckpt:
                ckpt.write("Done"+"\n")
                ckpt.close()

        lifted_coarse_dir = iter_dir + "/L_coarse_k_"+str(iteration)+"_n_"+str(time_slice)
        try:
            os.mkdir(lifted_coarse_dir)
            print("Directory created "+ lifted_coarse_dir)
        except FileExistsError as fe:
            print(lifted_coarse_dir + " already exist")
        utf.setup_fine(opt.src_case_fine,lifted_coarse_dir)
        utf.modify_control_param(lifted_coarse_dir,{"startTime":ts_tpl[time_slice-1][1],"endTime":ts_tpl[time_slice-1][1]})
        try:
            shutil.rmtree(lifted_coarse_dir+"/0")
        except FileNotFoundError as fn:
            print(lifted_coarse_dir+"/0"+" alredy deleted")
        
        utf.run_mapfield(src="../../"+target_coarse_dir,dst=lifted_coarse_dir)
        # to prevent redo mapfield and resetup the fine dir
        if not os.path.exists(lifted_coarse_dir+"/checkpoint.txt"):
            with open(lifted_coarse_dir + "/checkpoint.txt","w+") as ckpt:
                ckpt.write("Done"+"\n")
                ckpt.close()


        target_fine_dir = fine_bar_dir +'/'+opt.dir_timeslice+str(time_slice + 1)

        project_banner = """

 {}         {}        {}          {}  
F    =   L(C  )  +   F    -  L(R(F  ))
 {}         {}        {}          {}  
        
        """.format(time_slice,time_slice,time_slice,time_slice,iteration,iteration,iteration-1,iteration-1)
        print(project_banner)
        print("["+target_fine_dir+"] = ["+lifted_coarse_dir +"] + ["+prev_fine_bar+"] - ["+lifted_restrict_fine_bar_dir+"]")
        prj.add_projection(lifted_coarse_dir,prev_fine_bar,lifted_restrict_fine_bar_dir,ts_tpl,time_slice,target_fine_dir)
       

