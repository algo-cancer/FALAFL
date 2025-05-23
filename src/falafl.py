#!/usr/bin/env python



import gurobipy as gp, numpy as np, math
import sys, os, argparse


def falafl(S,q,c,t):
    n,m = S.shape
    

    model = gp.Model()
    model.Params.Threads = c
    model.Params.TimeLimit = t

    # initialize variables
    R = np.empty(m,dtype=object)
    for j in range(m): 
        R [j]= model.addVar(vtype=gp.GRB.BINARY)

    # set constraints

    for i in range(n):
        model.addConstr(gp.quicksum(R[j]*S[i,j] for j in range(m)) >= q* gp.quicksum(R[j] for j in range(m)))

      

    # set objective
    model.setObjective(gp.quicksum(R[j]* S[i,j] for j in range(m) for i in range(n)), gp.GRB.MAXIMIZE)

    model.optimize()

    return np.array([j for j in range(m) if R[j].X > 0])



def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_binary', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=True)
    parser.add_argument('-q', '--q', type=float, required=True)
    parser.add_argument('-c', '--threads', type=int, required=True)
    parser.add_argument('-t', '--run_time', type=int, required=True)
    
    return parser
  
def main():
    args = get_parser().parse_args(sys.argv[1:])
    assert args.q <= 1

    S = np.load(args.input_binary, allow_pickle=True)['m']

   # run falafl
    R_chosen = falafl(S,args.q,args.threads, args.run_time)
    np.savez(args.output,  cols=R_chosen )
    print(len(R_chosen))
    print(S.shape[1])


if __name__=="__main__":
    #parser
    main()
