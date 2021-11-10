# Algorithm



$T_0^0 = T_0$

$T_0^{n+1} = G_{\Delta t}(T_0^n)$

$\bold T_0^n = \mathcal L(T_0^n)$



$\bar T_k^{n+1} = G_{\Delta t} (T_k^n) $

$\bold {\bar T_k^{n+1}} = F_{\Delta t} (\bold T_k^n) $

$T_{k+1}^{n+1} = G_{\Delta t} T_{k+1}^n + ( R(\bar{\bold{T}}_k^{n+1}) - \bar{T}_k^{n+1})$

$\bold{T}_{k+1}^{n+1} = L(T_{k+1}^{n+1}) + (\bar{\bold{T}}_k^{n+1} - L(R(\bar {\bold{T}}_k^{n+1}) )$

## Expanded for k = 0

From first two lines 

$T_0^0,T_0^1,T_0^2,T_0^3,T_0^4,T_0^5,T_0^6,T_0^7,T_0^8,T_0^9,T_0^{10}$

using line 3 lifting operation

$\bold T_0^0,\bold T_0^1,\bold T_0^2,\bold T_0^3,\bold T_0^4,\bold T_0^5,\bold T_0^6,\bold T_0^7,\bold T_0^8,\bold T_0^9,\bold T_0^{10}$



$\bar T_0^1 = G_{\Delta t}(T_0^0) = T_0^1 \\ \bar T_0^2 = G_{\Delta t}(T_0^1)=T_0^2 \\ \vdots \\ \bar T_0^{10} = G_{\Delta t}(T_0^9)=T_0^{10}$

 0,     5,    10,  15,  20,  25,  30,  35,  40,  45,  50

$\bold T_0^0,\bold T_0^1,\bold T_0^2,\bold T_0^3,\bold T_0^4,\bold T_0^5,\bold T_0^6,\bold T_0^7,\bold T_0^8,\bold T_0^9,\bold T_0^{10}$

$T_0^0,\bar T_0^1,\bar T_0^2,\bar T_0^3,\bar T_0^4,\bar T_0^5,\bar T_0^6,\bar T_0^7,\bar T_0^8,\bar T_0^9,\bar T_0^{10} \\ \shortparallel \\ T_0^0,T_0^1,T_0^2,T_0^3,T_0^4,T_0^5,T_0^6,T_0^7,T_0^8,T_0^9,T_0^{10} $





$\bold {\bar T_0^1} = F_{\Delta t}(\bold T_0^0) , \bold {\bar T_0^2} = F_{\Delta t}(\bold T_0^1) , \dots , \bold {\bar T_0^{10}} = F_{\Delta t}(\bold T_0^9)$



$T_1^0 = T_0^0$

${T_1^1} = G_{\Delta t} T_{1}^0 + ( R(\bar{\bold{T}}_0^{1}) - \bar{T}_0^{1})$

$\bold{T}_{1}^{1} = L(T_{1}^{1}) + (\bar{\bold{T}}_0^{1} - L(R(\bar {\bold{T}}_0^{1}) )$



${T_1^2} = G_{\Delta t} T_{1}^1 + ( R(\bar{\bold{T}}_0^{2}) - \bar{T}_0^{2})$

$\bold{T}_{1}^{2} = L(T_{1}^{2}) + (\bar{\bold{T}}_0^{2} - L(R(\bar {\bold{T}}_0^{2}) )$



K =0

initial coarse  $T_0^0,T_0^1,T_0^2,T_0^3,T_0^4,T_0^5,T_0^6,T_0^7,T_0^8,T_0^9,T_0^{10}$

coarse bar     TS_1 = $(T_0^0 , \bar T_0^1)$ , TS_2 = $(T_0^1 , \bar T_0^2)$, TS_3 = $(T_0^2 , \bar T_0^3)$,     $\dots$     , TS_10 = $(T_0^9 , \bar T_0^{10})$             

fine bar          TS_1 = $(\bold T_0^0 ,\bold {\bar T_0^1})$ , TS_2 = $(\bold T_0^1 ,\bold{\bar T_0^2})$, TS_3 = $(\bold T_0^2 , \bold{\bar T_0^3})$,    $\dots$     , TS_10 = $(\bold T_0^9 ,\bold{ \bar T_0^{10}})$



k =1

coarse bar    TS_1 = $(T_1^0 , \bar T_1^1)$

fine bar          TS_1 = $(\bold T_1^0)$ 





  lifting             restrict

interpolate interpolate fail 2nd iteration

interpolate cellpointinterpolate fail

cellpointinterpolate   interpolate  fail

cellpointinterpolate   cellpointinterpolate   fail

interpolate mapNearest    success

cellpointinterpolate    mapNearest     fail

mapnearest    interpolate fail

mapnearest  cellpointinterpolate fail









Re = d*U / nu

d := diameter of the cylinder
U := velocity
nu := viscosity

right now we have:

Re = 2*1*10^3 = 2000



norm(uref - uparareal) / norm( uref )
