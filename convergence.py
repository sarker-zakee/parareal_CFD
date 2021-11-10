
from typing import Dict
import numpy as np
from numpy.lib.function_base import average
import options as opt
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile as ppf
import re


def allvar_ref(refrence):
    iter_start = 0

    iter_dir = opt.dir_iteration + str(iter_start)
    vars = dict()
    files = ["epsilon","k","nut","p","U"]
    for ff in files:
        v =[]
        for t in range(1,opt.end_time+1):
            path = refrence + "/" + str(t) + '/'+ ff
            f = open(path,'r')
            # print(path)
            s = f.read()
            # Remove comments like "//" until end of line
            s = re.sub(r'//.*', '', s)

            # Remove comments between /* and */
            s = re.sub(r'/\*(.|\s)*?\*/', '', s, re.DOTALL)

            r1 = re.search(r'23200\n\(\n((.*\n){23200})\)',s)
            if ff == "U":
                data = [[[float(v[0])],[float(v[2])],[float(v[4])]]
            for v in re.findall(r'\(([+-]?[0-9.]*([eE][+-]?[0-9]*)?)\s([+-]?[0-9.]*([eE][+-]?[0-9]*)?)\s([+-]?[0-9.]*([eE][+-]?[0-9]*)?)\)', r1.group(1))]
            else:
                data = [float(item) for item in re.findall(r"([+-]?[0-9.]*[eE]?[+-]?[0-9]*?)\s",r1.group(1))]
            v.append(np.array(data))
        vars[ff] = np.stack(v)
        
    # print(vars)
    np.savez(refrence+"/internalFields",epsilon = vars["epsilon"],k = vars["k"],nut=vars["nut"],p=vars["p"],U=vars["U"])
    print(refrence+"/internalFields.npz saved")





def allvar_iteration(fine_bar_path):
    vars = dict()
    files = ["epsilon","k","nut","p","U"]
    for ff in files:
        v =[]
        for i in range(1,opt.number_time_slice+1):
            end = i*5+1
            begin = end-5
            for j in range(begin,end):
                path = fine_bar_path + "/" + opt.dir_timeslice + str(i) + "/" + str(j) + "/" + ff
                # print(path)
                f = open(path,'r')
                s = f.read()
                # Remove comments like "//" until end of line
                s = re.sub(r'//.*', '', s)

                # Remove comments between /* and */
                s = re.sub(r'/\*(.|\s)*?\*/', '', s, re.DOTALL)

                r1 = re.search(r'23200\n\(\n((.*\n){23200})\)',s)
                if ff == "U":
                    data = [[[float(v[0])],[float(v[2])],[float(v[4])]]
                for v in re.findall(r'\(([+-]?[0-9.]*([eE][+-]?[0-9]*)?)\s([+-]?[0-9.]*([eE][+-]?[0-9]*)?)\s([+-]?[0-9.]*([eE][+-]?[0-9]*)?)\)', r1.group(1))]
                else:
                    data = [float(item) for item in re.findall(r"([+-]?[0-9.]*[eE]?[+-]?[0-9]*?)\s",r1.group(1))]
                v.append(np.array(data))
        vars[ff] = np.stack(v)
    np.savez(fine_bar_path+"/internalFields",epsilon = vars["epsilon"],k = vars["k"],nut=vars["nut"],p=vars["p"],U=vars["U"])
    print(fine_bar_path+"/internalFields.npz saved")



def convergence_check(ref_var,iterate_var,iter_counter):

    ref_variables = np.load(ref_var+"/internalFields.npz")
    iter_variables = np.load(iterate_var+"/internalFields.npz")

    files = ["epsilon","k","nut","p","U"]
    var_l2_norms = dict()
    l2_relative_error = dict()
    var_max_norms = dict()
    max_relative_error = dict()
    for f in files:
        l2_norm=[]
        l2_rel_error =[]
        max_norm=[]
        max_rel_error = []
        for t in range(opt.start_time,opt.end_time):
            l2 = np.linalg.norm(ref_variables[f][t]-iter_variables[f][t])
            rel = l2 / np.linalg.norm(ref_variables[f][t])
            mx = np.linalg.norm(np.ravel(ref_variables[f][t]-iter_variables[f][t]),ord=np.inf)    
            rel_mx = mx / np.linalg.norm(np.ravel(ref_variables[f][t]),ord=np.inf)
            l2_norm.append(l2)
            l2_rel_error.append(rel)
            max_norm.append(mx)
            max_rel_error.append(rel_mx)

        var_l2_norms[f] = np.array(l2_norm)
        l2_relative_error[f] = np.array(l2_rel_error)
        var_max_norms[f] = np.array(max_norm)
        max_relative_error[f] = np.array(max_rel_error)

        print("file : {}, avg l2_norm : {}, avg rel error : {}".format(f,np.average(var_l2_norms[f]),np.average(l2_relative_error[f]))) 
        
    np.savez(iterate_var.split('/')[0]+"/L2_dist",epsilon = var_l2_norms["epsilon"],k = var_l2_norms["k"],nut=var_l2_norms["nut"],p=var_l2_norms["p"],U=var_l2_norms["U"])
    print(iterate_var.split('/')[0]+"/L2_dist.npz saved")

    np.savez(iterate_var.split('/')[0]+"/L2_rel_error",epsilon = l2_relative_error["epsilon"],k = l2_relative_error["k"],nut=l2_relative_error["nut"],p=l2_relative_error["p"],U=l2_relative_error["U"])
    print(iterate_var.split('/')[0]+"/L2_rel_error.npz saved")

    np.savez(iterate_var.split('/')[0]+"/max_dist",epsilon = var_max_norms["epsilon"],k = var_max_norms["k"],nut=var_max_norms["nut"],p=var_max_norms["p"],U=var_max_norms["U"])
    print(iterate_var.split('/')[0]+"/max_dist.npz saved")

    np.savez(iterate_var.split('/')[0]+"/max_rel_error",epsilon = max_relative_error["epsilon"],k = max_relative_error["k"],nut=max_relative_error["nut"],p=max_relative_error["p"],U=max_relative_error["U"])
    print(iterate_var.split('/')[0]+"/max_rel_error.npz saved")


    

    if iter_counter == 0:
        return True
    elif iter_counter >0:
        prev_l2_relative_error = np.load(opt.dir_iteration+str(iter_counter-1)+'/'+"L2_rel_error.npz")
        files = ["epsilon","k","nut","p","U"]
        avg_diff=[]
        for f in files:
            avg_diff.append(np.average(prev_l2_relative_error[f])-np.average(l2_relative_error[f]))
            
        if sum(avg_diff)== 0:
            return False
        else:
            return True

    # if np.average(var_l2_norms['epsilon']) < opt.L2_norm_tolarance and np.average(var_l2_norms['k']) < opt.L2_norm_tolarance:
    #     return False
    # else:
    #     return True

# allvar_ref("ref_run_fine")
# allvar_iteration("K_0/fine_bar")
# convergence_check("ref_run_fine","K_0/fine_bar")