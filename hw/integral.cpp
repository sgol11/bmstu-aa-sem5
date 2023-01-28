long double calculate_integral(interval_t &interval, function_t func)
{
    unsigned long n = 2;                                         // 1
    long double delta = 1;                                       // 2
    long double res = 0, obt_res = 0;                            // 3
    double step, x;                                              // 4

    while (delta > interval.eps)                                 // 5
    {
        res = obt_res;                                           // 6
        obt_res = 0;                                             // 7

        step = (interval.end - interval.begin) / n;              // 8
        x = interval.begin;                                      // 9

        while (x < interval.end - step)                          // 10
        {
            obt_res += 0.5 * step * (func(x) + func(x + step));  // 11
            x += step;                                           // 12
        }
        
        n *= 2;                                                  // 13
        delta = abs(res - obt_res);                              // 14
    }

    return res;
}