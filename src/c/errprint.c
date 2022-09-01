#include "msgprint.h"

#define DBG_BUF_LEN  1024

static TDbgFuncW wc_dbg_func = NULL;   /* Debug function using wide characters  */
static TDbgFunc dbg_func = NULL;      /* Debug function using normal characters */

static wchar_t  wc_buffer[DBG_BUF_LEN];
static char buffer[DBG_BUF_LEN];



void  msgprint(const char *s, ...)
{

    if (dbg_func != NULL){
        va_list va;
        va_start(va, s);
        vsprintf_s(buffer, DBG_BUF_LEN, s, va);
        va_end(va);
        dbg_func(buffer);
    }
}



void SetMsgFunc(TDbgFunc p)
{
    dbg_func = p;
}



