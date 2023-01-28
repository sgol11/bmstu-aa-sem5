#ifndef INTEGRAL_H
#define INTEGRAL_H

#include <iostream>
#include <vector>
#include <cmath>
#include <thread>
#include <mutex>
#include <iomanip>

using namespace std;

struct interval_t
{
    double begin;
    double end;
    double eps;
};

typedef long double(*function_t)(double);

long double midpoint(double begin, double end, unsigned int n, function_t func);
long double trapezoidal(double begin, double end, unsigned int n, function_t func);

long double calculate_integral(interval_t &interval, function_t func, long double (&method)(double, double, unsigned int, function_t));

void midpoint_parallel(double begin, double end, unsigned int n, function_t func,
                       long double &res, int threads_num, int i, mutex &mut);
void trapezoidal_parallel(double begin, double end, unsigned int n, function_t func,
                          long double &res, int threads_num, int i, mutex &mut);

long double calculate_integral_parallel(int threads_num, interval_t &interval, function_t func,
                                        void (&method)(double, double, unsigned int, function_t, long double &, int, int, mutex &));

#endif // INTEGRAL_H
