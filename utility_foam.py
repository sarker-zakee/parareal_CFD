from genericpath import isdir
import os
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
import subprocess
import options as opt
import multiprocessing as mp

def run_openfoam(folder):

    if os.path.exists(folder+"/checkpoint.txt") and  os.path.isfile(folder+"/checkpoint.txt"):
        with open(folder+"/checkpoint.txt","r") as ckpt:
            line = ckpt.readline()
            if line.rstrip('\n') == "Done":
                return
            
    if not(os.path.isdir(folder+"/log/")):
        os.mkdir(folder+"/log/")

    p1  = subprocess.Popen(['blockMesh','-case',folder],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = p1.communicate()

    if p1.returncode != 0:
        with open(folder+"/log/"+"blockMesh_error.log",'w+') as elog:
            elog.write(stderr.decode('utf-8').rstrip('\n'))
        # print(stderr.decode('utf-8').rstrip('\n'))
    else:
        with open(folder+"/log/"+"blockMesh_run.log",'w+') as rlog:
            rlog.write(stdout.decode('utf-8').rstrip('\n'))
        # print(stdout.decode('utf-8').rstrip('\n'))
    
    p1.wait()   

    p2  = subprocess.Popen(['pisoFoam','-case',folder],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = p2.communicate()

    if p2.returncode != 0:
        with open(folder+"/log/"+"pisoFoam_error.log",'w+') as elog:
            elog.write(stderr.decode('utf-8').rstrip('\n'))
        # print(stderr.decode('utf-8').rstrip('\n'))
    else:
        with open(folder+"/log/"+"pisoFoam_run.log",'w+') as rlog:
            rlog.write(stdout.decode('utf-8').rstrip('\n'))
        # print(stdout.decode('utf-8').rstrip('\n'))
    
    p2.wait() 

    if p1.returncode == 0 and p2.returncode ==0 :
        print("successfully run pisofoam in "+folder )
        with open(folder + "/checkpoint.txt","w+") as ckpt:
            ckpt.write("Done"+"\n")
            ckpt.close()
    else: 
        exit("error occure during run_OpenFoam "+folder)

    
def modify_control_param(case_dir,pv_dict):
    f = ParsedParameterFile(os.path.join(case_dir,"system","controlDict"))
    for k in pv_dict.keys():
        f[k] = pv_dict[k]
    f.writeFile()


# interpolate, mapNearest , cellPointInterpolate
def run_mapfield(src,dst,mapmethod="mapNearest"):

    if os.path.exists(dst+"/log/"+"mapfield_run.log") and  os.path.isfile(dst+"/log/"+"mapfield_run.log"):
        print("mapField already ran")
        return
    
    if not(os.path.isdir(dst+"/log/")):
        os.mkdir(dst+"/log/")

    p1 = subprocess.Popen(['mapFields',src,'-consistent','-mapMethod',mapmethod], cwd=dst,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p1.communicate()

    if p1.returncode != 0:
        with open(dst+"/log/"+"mapfield_error.log",'w+') as elog:
            elog.write(stderr.decode('utf-8').rstrip('\n'))
        # print(stderr.decode('utf-8').rstrip('\n'))
    else:
        with open(dst+"/log/"+"mapfield_run.log",'w+') as rlog:
            rlog.write(stdout.decode('utf-8').rstrip('\n'))
            print("---------------------------------------------------------------------------------------------")
            kw = ["Exec","Source","Target","mapping","Source:","Target:"]
            rlog.seek(0)
            lines = [x.rstrip('\n') for x in iter(rlog.readlines())]
            for line in lines:
                if any(word in line.split() for word in kw):
                    print(line)
            print("---------------------------------------------------------------------------------------------")
        # print(stdout.decode('utf-8').rstrip('\n'))


def setup_coarse(coarse_src_dir,target_dir):

    if os.path.exists(target_dir+"/checkpoint.txt") and  os.path.isfile(target_dir+"/checkpoint.txt"):
        with open(target_dir+"/checkpoint.txt","r") as ckpt:
            line = ckpt.readline()
            if line.rstrip('\n') == "Done":
                return
    orig = SolutionDirectory ( coarse_src_dir , archive = None ,paraviewLink = False )
    target_case = orig.cloneCase ( target_dir )
    write_interval = ((opt.end_time - opt.start_time) / opt.dt_coarse ) / opt.number_time_slice
    modify_control_param(target_case.name,{"writeInterval":write_interval})



def setup_fine(fine_src_dir,target_dir):

    if os.path.exists(target_dir+"/checkpoint.txt") and  os.path.isfile(target_dir+"/checkpoint.txt"):
        with open(target_dir+"/checkpoint.txt","r") as ckpt:
            line = ckpt.readline()
            if line.rstrip('\n') == "Done":
                return
    
    orig = SolutionDirectory ( fine_src_dir , archive = None ,paraviewLink = False )
    target_case = orig.cloneCase ( target_dir )

    coarse_write_interval = ((opt.end_time - opt.start_time)/opt.dt_coarse) / opt.number_time_slice
    num_intermediate_steps = opt.min_number_times_per_timestep
    while (coarse_write_interval % num_intermediate_steps) != 0:
        num_intermediate_steps = num_intermediate_steps + 1
    write_interval = coarse_write_interval / num_intermediate_steps
    modify_control_param(target_case.name,{"writeInterval":write_interval})


def runfoam_all_timeslice(dir):
    params = [os.path.join(dir,x) for x in os.listdir(dir) if os.path.isdir(os.path.join(dir,x))]
    with mp.Pool(mp.cpu_count()) as p:
        p.map(run_openfoam, params)