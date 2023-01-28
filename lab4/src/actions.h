#ifndef ACTIONS_H
#define ACTIONS_H

#include "integral.h"

enum action_t
{
    EXIT,
    SINGLE,
    MASS,
    BEGIN
};

void single(int &ch);
void mass(int &ch);

#endif // ACTIONS_H
