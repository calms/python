@echo off
setlocal

REM echo "#%1"

if "%1%"=="t" goto testTail
if "%1%"=="T" goto testTail
if "%1%"=="T2" goto testTail2
if "%1%"=="t2" goto testTail2
if "%1%"=="1" goto warsaw
if "%1%"=="2" goto crystal
if "%1%"=="3" goto dtca
if "%1%"=="4" goto german
if "%1%"=="5" goto idns
if "%1%"=="6" goto rdfc
if "%1%"=="7" goto template
if "%1%"=="8" goto spain
REM goto testTailInput
goto other

:testTail
REM echo test Tail
cmd /c type leapLog2GMI.py | python - "testTailMon.log" "0" > D:\Reuters\LEAP_Log_Monitor\logs\LEAP_mon_TEST_Scheduler.log 2>>&1
goto next

:testTail2
REM echo test Tail2
cmd /c type "D:\Reuters\LEAP_Log_Monitor\leapLog2GMI.py" | python - "testTailMon_Second.log" "0" "D:\Reuters\LEAP_Log_Monitor" "D:\Reuters\LEAP_Log_Monitor\logs" > D:\Reuters\LEAP_Log_Monitor\logs\LEAP_mon_TEST2_Scheduler.log 2>>&1
goto next

:testTailInput
REM echo test Tail
cmd /c type "D:\Reuters\LEAP_Log_Monitor\leapLog2GMI.py" | python - "%1%" "-" "D:\Reuters\LEAP_Log_Monitor" "D:\Reuters\LEAP_Log_Monitor\logs\logs" > D:\Reuters\LEAP_Log_Monitor\logs\LEAP_mon_TEST_Scheduler.log 2>>&1
goto next

:warsaw
REM echo warsaw
REM cmd /c type D:\Reuters\LEAP_Log_Monitor\leapLog2GMI.py | python - "testTailMon.log" "1" "1>D:\Reuters\LEAP_Log_Monitor\logs\LEAP_mon_WARS_Scheduler.log 2>>&1"
cmd /c type "D:\Reuters\LEAP_Log_Monitor\leapLog2GMI.py" | python - "testTailMon.log"  "1" >D:\Reuters\LEAP_Log_Monitor\logs\LEAP_mon_WARS_Scheduler.log 2>>&1
goto next

:crystal
REM echo crystal
REM cmd /c type "D:\Reuters\LEAP_Log_Monitor\leapLog2GMI.py" | python - "testTailMon.log" "2" "1>D:\Reuters\LEAP_Log_Monitor\logs\LEAP_mon_CRYS_Scheduler.log 2>>&1"
cmd /c type "D:\Reuters\LEAP_Log_Monitor\leapLog2GMI.py" | python - "testTailMon.log" "2" >D:\Reuters\LEAP_Log_Monitor\logs\LEAP_mon_CRYS_Scheduler.log 2>>&1
goto next

:dtca
REM echo dtca
cmd /c type "D:\Reuters\LEAP_Log_Monitor\leapLog2GMI.py" | python - "testTailMon.log" "3" >D:\Reuters\LEAP_Log_Monitor\logs\LEAP_mon_DTCA_Scheduler.log 2>>&1
goto next

:german
REM echo german
cmd /c type "D:\Reuters\LEAP_Log_Monitor\leapLog2GMI.py" | python - "testTailMon.log" "4" >D:\Reuters\LEAP_Log_Monitor\logs\LEAP_mon_GERM_Scheduler.log 2>>&1
goto next

:idns
REM echo idns
cmd /c type "D:\Reuters\LEAP_Log_Monitor\leapLog2GMI.py" | python - "testTailMon.log" "5" >D:\Reuters\LEAP_Log_Monitor\logs\LEAP_mon_IDNS_Scheduler.log 2>>&1
goto next

:rdfc
REM echo rdfc
cmd /c type "D:\Reuters\LEAP_Log_Monitor\leapLog2GMI.py" | python - "testTailMon.log" "6" >D:\Reuters\LEAP_Log_Monitor\logs\LEAP_mon_RDFC_Scheduler.log 2>>&1
goto next

:template
REM echo template
cmd /c type "D:\Reuters\LEAP_Log_Monitor\leapLog2GMI.py" | python - "testTailMon.log" "7" >D:\Reuters\LEAP_Log_Monitor\logs\LEAP_mon_TMPL_Scheduler.log 2>>&1
goto next

:spain
REM echo spain
cmd /c type "D:\Reuters\LEAP_Log_Monitor\leapLog2GMI.py" | python - "testTailMon.log" "8" >D:\Reuters\LEAP_Log_Monitor\logs\LEAP_mon_SPAIN_Scheduler.log 2>>&1
goto next

:other
REM echo other
echo Usage: %0 2
goto next

:next
REM echo END
exit /b 1
endlocal