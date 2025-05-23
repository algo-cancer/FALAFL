#!/usr/bin/env python


import numpy as np, math
import sys, os, argparse

def first_preprocessing(m,delta):
  to_rm = set(np.where(m<delta)[1])
  to_keep = sorted(set(range(m.shape[1])) - to_rm)
  
  m = m[:,to_keep]
  return m

def second_preprocessing(m,p):
  m[m< p]  = 0
  m[m>=p] = 1
  return m

def third_preprocessing(m,k):
  counts = np.sum(m,axis=0)
  to_keep = np.where(counts>=k)[0]
  m  = m[:,to_keep]
  return m
  
  
def get_parser():
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input', type=str, required=True)
  parser.add_argument('-o', '--output', type=str, required=True)
  parser.add_argument('-p', '--p', type=float, required=True)
  parser.add_argument('-k', '--k', type=int, required=True)
  parser.add_argument('-d', '--delta', type=float, required=False,default =None)
    
  return parser


def main():
  args = get_parser().parse_args(sys.argv[1:])
  assert args.q <= 1

  S = np.load(args.input, allow_pickle=True)['m']

  if args.delta!=None:
    delta = args.delta
    _S = first_preprocessing(S,delta)

  else:
    _S = second_preprocessing(S,p)

  _S_final = third_preprocessing(_S,k) 



  np.savez(args.output,  m=_S_final )
  print(len(R_chosen))
  print(S.shape[1])


if __name__=="__main__":
  #parser
  main()
