from typing import Dict
import utility_foam as utf
import shutil , os 
import options as opt 
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile as ppf
from PyFoam.Basics.DataStructures import Dimension,Field,Vector
from deepdiff import DeepDiff
import numpy as np

def add_projection(lifted_coarse_dir,prev_fine_bar,lifted_restrict_fine_bar_dir,ts_tpl,time_slice,target_fine_dir):
    already_created = False
    try:
        os.mkdir(target_fine_dir)
        print("Directory created "+ target_fine_dir)
    except FileExistsError as fe:
        print(target_fine_dir + " already exist")
        already_created = True
    
    if not already_created :
        utf.setup_fine(opt.src_case_fine,target_fine_dir)
        utf.modify_control_param(target_fine_dir,{"startTime":ts_tpl[time_slice][0],"endTime":ts_tpl[time_slice][1]})
        try:
            shutil.rmtree(target_fine_dir+"/0")
        except FileNotFoundError as fn:
            print(target_fine_dir+"/0"+" alredy deleted")
    
    target_time_dir = ts_tpl[time_slice][0]

    src = lifted_coarse_dir +'/'+str(target_time_dir)
    dst = target_fine_dir  +'/'+str(target_time_dir)

    try:
        os.mkdir(dst)
        print("Directory created "+ dst)
    except FileExistsError as fe:
        print(dst + " already exist")


    files = ['epsilon','k','p','U','nut']

    for f in files:
        
        # if not os.path.isfile(dst+'/'+f):
        #     shutil.copy2(src+'/'+f,dst+'/'+f)
        shutil.copy2(src+'/'+f,dst+'/'+f)
        
    for f in files:

        lifted_coarse = dst + '/' + f
        fine_bar = prev_fine_bar+'/'+str(target_time_dir)+ '/' + f
        l_r_fine_bar = lifted_restrict_fine_bar_dir +'/'+str(target_time_dir)+ '/' + f


        target_file = ppf(lifted_coarse)
        x = target_file.getValueDict()
        y = ppf(fine_bar).getValueDict()
        z = ppf(l_r_fine_bar).getValueDict()

        if f == 'epsilon':
            all_equal=[]
            if x['dimensions'] == y['dimensions'] == z['dimensions']:
                all_equal.append(True)
                # print("all dimensions equal with value "+ str(x['dimensions']))
            
            xval = np.array(x['internalField'].val)
            yval = np.array(y['internalField'].val)
            zval = np.array(z['internalField'].val)
              
            newval = xval + yval - zval

            for item in ['inlet','outlet','cylinder','top','bottom','FrontAndBack']:
                if x['boundaryField'][item]['type'] == y['boundaryField'][item]['type'] == z['boundaryField'][item]['type']:
                    all_equal.append(True)
                    # print('all type field equal for '+item+" with value "+x['boundaryField'][item]['type'])

            if x['boundaryField']['inlet']['value'].val == y['boundaryField']['inlet']['value'].val== y['boundaryField']['inlet']['value'].val:
                all_equal.append(True)
                # print('all inlet value field equal with val '+str(x['boundaryField']['inlet']['value'].val))

            xval_cylinder = np.array(x['boundaryField']['cylinder']['value'].val)
            yval_cylinder = np.array(y['boundaryField']['cylinder']['value'].val)
            zval_cylinder = np.array(z['boundaryField']['cylinder']['value'].val)


            newval_cylinder = xval_cylinder + yval_cylinder - zval_cylinder

            x['internalField'].val = list(newval)
            x['boundaryField']['cylinder']['value'].val = list(newval_cylinder)
            if all(all_equal):
                target_file.writeFile()
                print(f)
        
        elif f == 'k':
            all_equal=[]
            if x['dimensions'] == y['dimensions'] == z['dimensions']:
                all_equal.append(True)
                # print("all dimensions equal with value "+ str(x['dimensions']))
            
            xval = np.array(x['internalField'].val)
            yval = np.array(y['internalField'].val)
            zval = np.array(z['internalField'].val)
              
            newval = xval + yval - zval

            for item in ['inlet','outlet','cylinder','top','bottom','FrontAndBack']:
                if x['boundaryField'][item]['type'] == y['boundaryField'][item]['type'] == z['boundaryField'][item]['type']:
                    all_equal.append(True)
                    # print('all type field equal for '+item+" with value "+x['boundaryField'][item]['type'])
                if item == 'inlet' or item == 'cylinder':
                    if x['boundaryField'][item]['value'].val == y['boundaryField'][item]['value'].val== y['boundaryField'][item]['value'].val:
                        all_equal.append(True)
                        # print('all '+item+' value field equal with val '+str(x['boundaryField'][item]['value'].val))
            
            x['internalField'].val = list(newval)
            if all(all_equal):
                target_file.writeFile()
                print(f)
        elif f == 'p':
            all_equal = []
            if x['dimensions'] == y['dimensions'] == z['dimensions']:
                all_equal.append(True)
                # print("all dimensions equal with value "+ str(x['dimensions']))
            
            xval = np.array(x['internalField'].val)
            yval = np.array(y['internalField'].val)
            zval = np.array(z['internalField'].val)
              
            newval = xval + yval - zval

            for item in ['inlet','outlet','cylinder','top','bottom','FrontAndBack']:
                if x['boundaryField'][item]['type'] == y['boundaryField'][item]['type'] == z['boundaryField'][item]['type']:
                    all_equal.append(True)
                    # print('all type field equal for '+item+" with value "+x['boundaryField'][item]['type'])
                if item == 'outlet':
                    if x['boundaryField'][item]['value'].val == y['boundaryField'][item]['value'].val== y['boundaryField'][item]['value'].val:
                        all_equal.append(True)
                        # print('all '+item+' value field equal with val '+str(x['boundaryField'][item]['value'].val))
            
            x['internalField'].val = list(newval)
            if all(all_equal):
                target_file.writeFile()
                print(f)

        elif f == 'U':
            all_equal=[]
            if x['dimensions'] == y['dimensions'] == z['dimensions']:
                all_equal.append(True)
                # print("all dimensions equal with value "+ str(x['dimensions']))

            xval = np.array(x['internalField'].val)
            yval = np.array(y['internalField'].val)
            zval = np.array(z['internalField'].val)

            newval = xval + yval - zval

            for item in ['inlet','outlet','cylinder','top','bottom','FrontAndBack']:
                if x['boundaryField'][item]['type'] == y['boundaryField'][item]['type'] == z['boundaryField'][item]['type']:
                    all_equal.append(True)
                    # print('all type field equal for '+item+" with value "+x['boundaryField'][item]['type'])
                if item == 'inlet':
                    for i in ["fluctuationScale","referenceField","alpha"]:
                        if x['boundaryField'][item][i] == y['boundaryField'][item][i] == z['boundaryField'][item][i]:
                            all_equal.append(True)
                            # print('all '+i+' field equal for '+item+" with value "+str(x['boundaryField'][item][i]))
                if item == 'outlet':
                    if x['boundaryField'][item]['inletValue'] == y['boundaryField'][item]['inletValue'] == z['boundaryField'][item]['inletValue']:
                        all_equal.append(True)
                        # print('all inletValue field equal for '+item+" with value "+str(x['boundaryField'][item]['inletValue']))

            xval_inlet = np.array(x['boundaryField']['inlet']['value'].val)
            yval_inlet = np.array(y['boundaryField']['inlet']['value'].val)
            zval_inlet = np.array(z['boundaryField']['inlet']['value'].val)

            newval_inlet = xval_inlet + yval_inlet - zval_inlet
            
            xval_outlet = np.array(x['boundaryField']['outlet']['value'].val)
            yval_outlet = np.array(y['boundaryField']['outlet']['value'].val)
            zval_outlet = np.array(z['boundaryField']['outlet']['value'].val)

            newval_outlet = xval_outlet + yval_outlet - zval_outlet

        
            
            x['internalField'].val = [Vector(x,y,z) for x,y,z in newval]
            x['boundaryField']['inlet']['value'].val =[Vector(x,y,z)for x,y,z in  newval_inlet]
            x['boundaryField']['outlet']['value'].val = [Vector(x,y,z)for x,y,z in newval_outlet]
            if all(all_equal):
                target_file.writeFile()
                print(f)

        elif f == 'nut':
            all_equal=[]
            if x['dimensions'] == y['dimensions'] == z['dimensions']:
                all_equal.append(True)
                # print("all dimensions equal with value "+ str(x['dimensions']))

            xval = np.array(x['internalField'].val)
            yval = np.array(y['internalField'].val)
            zval = np.array(z['internalField'].val)

            newval = xval + yval - zval

            for item in ['inlet','outlet','cylinder','top','bottom','FrontAndBack']:
                if x['boundaryField'][item]['type'] == y['boundaryField'][item]['type'] == z['boundaryField'][item]['type']:
                    all_equal.append(True)
                    # print('all type field equal for '+item+" with value "+x['boundaryField'][item]['type'])
                if item == 'inlet':
                    if x['boundaryField'][item]['value'] == y['boundaryField'][item]['value'] == z['boundaryField'][item]['value']:
                        all_equal.append(True)
                        # print('all type field equal for '+item+" with value "+x['boundaryField'][item]['value'])
                if item == 'cylinder':
                     for i in ["value","Cmu","kappa","E"]:
                        if x['boundaryField'][item][i] == y['boundaryField'][item][i] == z['boundaryField'][item][i]:
                            all_equal.append(True)
                            # print('all '+i+' field equal for '+item+" with value "+str(x['boundaryField'][item][i]))
            
            x['internalField'].val = list(newval)
            if all(all_equal):
                target_file.writeFile()
                print(f)