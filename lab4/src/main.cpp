#include <iostream>

#include "integral.h"
#include "actions.h"

using namespace std;

#define HEADER "ИНТЕГРИРОВАНИЕ"

#define MENU_MSG \
"\nМЕНЮ\n\
1. Вычисление значения интеграла\n\
2. Сравнение последовательного и параллельного алгоритмов\n\
0. Выход\n\n\
Выбор: "

int main(void)
{
    cout << HEADER << endl;
    int ch = BEGIN;

    while (ch)
    {
        cout << MENU_MSG;
        cin >> ch;

        switch(ch)
        {
            case SINGLE:
                single(ch);
                break;
            case MASS:
                mass(ch);
                break;
            default:
                ch = 0;
        }
    }

    return 0;
}
