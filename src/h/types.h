#ifndef __types_h
  #define __types_h

/*********************************************************************
 * NAME     : types.h
 * ABSTRACT : The almost always obligatory types definition file
 *
 *********************************************************************/ 
 
#ifdef DEBUG
  #define MALLOC_CHECK_   2
#endif 

#include <stdio.h>

#ifdef _MSC_VER
 #include <malloc.h>
#else
 #include <malloc/malloc.h>
#endif
 
#include <assert.h>

#define FALSE    0
#define TRUE     1

/*
 *   Definition of some basic scalar type
 */
 
typedef unsigned int   ui32;
typedef signed int     si32;
typedef signed short   si16;
typedef unsigned short ui16;
typedef signed char    si8;
typedef unsigned char  ui8;

/*
 *   Definition of some basic geometric types in 3D space
 */
 
typedef struct{
   double x,y,z;
}TPoint3D;


typedef struct{
   double x,y,z;
}TVector3D;


typedef struct{
   double a,b,c;
}TLine3D;

typedef struct{
   double A,B,C,D;
}TPlane3D;


#endif
