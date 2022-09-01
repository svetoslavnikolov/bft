#include "msgprint.h"
#include <stdio.h>
#include <stdarg.h>

#define DBG_BUF_LEN  1024


static TMsgFunc msg_func = NULL;      /* Debug function using normal characters */

static char buffer[DBG_BUF_LEN];



void  msgprint(const char *s, ...)
{
    va_list va;
    va_start(va, s);
    vsnprintf(buffer, DBG_BUF_LEN, s, va);
    va_end(va);

    if (msg_func != NULL){
        msg_func(buffer);
    }
    else {
        printf(buffer);
    }
}



void SetMsgFunc(TMsgFunc p)
{
    msg_func = p;
}



