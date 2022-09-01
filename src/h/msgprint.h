/**
*   @file     msgprint.h
*   @Author   Svetoslav Nikolov (nikolov.svetoslav@gmail.com)
*   @date     October, 2014
*   @brief    Provides a mechanism for the application to use a callback
*             function which replaces "printf". 
*             The standard behavior is to use printf
*
*/

#pragma once

/** Definition of the callback "message" function */
typedef void(*TMsgFunc)(char* p);

void SetMsgFunc(TMsgFunc);

/** Call this function instead of printf */
void msgprint(const char* s, ...);       /* Handling 8-bit characters */
