import numpy as np
import matplotlib.pyplot as plt

import options as opt

start = 0
end = 10
files = ["epsilon","k","nut","U"]

# for f in files:
#     for i in range(start,end):
#         norm_file = opt.dir_iteration+str(i)+"/L2_dist.npz"
#         l = np.load(norm_file)
#         plt.plot(list(range(0,50)),l[f][0:50])
#         # plt.plot(list(range(0,50)),l[f][0:50],'.')
#         # plt.stackplot(list(range(0,50)),l[f],alpha=0.7)
#         plt.title(f+ " L2 norm ")
        
#     plt.legend(list(range(start,end)))
#     plt.show()


# for f in files:
#     rl_err = []
#     for i in range(start,end):
#         rel_err_file = opt.dir_iteration+str(i)+"/L2_rel_error.npz"
#         rele = np.load(rel_err_file)
#         print(i,f,np.average(rele[f]))
#         rl_err.append(np.average(rele[f]))
#         plt.plot(list(range(0,50)),rele[f][0:50])
#         # plt.plot(list(range(0,50)),l[f][0:50],'.')``
#         # plt.stackplot(list(range(0,50)),l[f],alpha=0.7)
#         plt.title(f + " relative error with l2 norm ")
        
#     plt.legend(list(range(start,end)))
#     print(np.min(rl_err))
#     print(f,[(round(x,5),round(y,5)) for x,y in zip(rl_err,rl_err[1:])])
#     print(f,[(x>y) for x,y in zip(rl_err,rl_err[1:])])
#     print(f,[round(x-y,5) for x,y in zip(rl_err,rl_err[1:])])
#     plt.show()


for f in files:
    rl_err = []
    for i in range(start,end):
        rel_err_file = opt.dir_iteration+str(i)+"/max_rel_error.npz"
        rele = np.load(rel_err_file)
        print(i,f,np.average(rele[f]))
        rl_err.append(np.average(rele[f]))
        plt.plot(list(range(0,50)),rele[f][0:50])
        # plt.plot(list(range(0,50)),l[f][0:50],'.')``
        # plt.stackplot(list(range(0,50)),l[f],alpha=0.7)
        plt.title(f + " relative error with max norm ")
        
    plt.legend(list(range(start,end)))
    print(np.min(rl_err))
    print(f,[(round(x,5),round(y,5)) for x,y in zip(rl_err,rl_err[1:])])
    print(f,[(x>y) for x,y in zip(rl_err,rl_err[1:])])
    print(f,[round(x-y,5) for x,y in zip(rl_err,rl_err[1:])])
    plt.show()
