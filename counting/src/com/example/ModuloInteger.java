package com.example;

public class ModuloInteger {
  public static int mod(int a, int p) {
    return a > 0 ? a % p : p + a % p;
  }
}
