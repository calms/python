################
##
##  Description:  This script tails a specified log file, searching for specific strings and generates GMI compliant log file using the strings found.
##  Author:  Nathaniel Achene
##  Date: 02 March 2015
##  
################

import re
import time
import socket
import os
from optparse import OptionParser
from datetime import datetime, date

SLEEP_INTERVAL = 1.0
sourceLogDir = "D:\\Logs" ##"C:\\scripts\\Reuters\\LEAP_Log_Monitor\\GVAP01" "C:\\temp\\LEAP\\DTCS-SPDAUTO01"
outputLogDir = "D:\\Reuters\\LEAP_Log_Monitor\\logs" ##"C:\\scripts\\Reuters\\LEAP_Log_Monitor\\GVAP01" 
fileGMI = outputLogDir + "\\LEAP_monitor_gmi.log"

def search_file_content(lineStr):
	today = datetime.now() 
	currTimeStamp = today.strftime("%Y-%m-%dT%H:%M:%S") # 2015-02-16T09:41:19        
	foundInfoWeb,foundInfoAuto,foundInfoWAR,foundInfoAUS,foundInfoQuant = [0,0,0,0,0]
	foundCriticalError,foundCriticalCRIT,foundCriticalExcep = [0,0,0]	
	searchObj = re.search( r'^\d{4}-\d{2}-.*', lineStr, re.M|re.I)  # re.M = match the strat/end of a line (not just the start/end of the string), re.I = ignorecase
	#file = open("LEAP_monitor_gmi.log", "a") #fileGMI
	if searchObj:
		foundCriticalError,foundCriticalCRIT,foundCriticalExcep = map(lineStr.find, ['ERROR','CRITICAL','Exception'])  # 'WARN'
		foundCriticalError = int(foundCriticalError)
		foundCriticalCRIT = int(foundCriticalCRIT)
		foundCriticalExcep = int(foundCriticalExcep)

		if ((foundCriticalError > 0) or (foundCriticalCRIT > 0) or (foundCriticalExcep > 0)):  ##if foundCriticalError > -1:
			knownInputDataErr, knownStartIndexErr, knownWarnInputErr = [0,0,0]
			knownKeyNotFound, knownFormatException, knownFailed, knownSeleniumFirefox, knownWebDriverException = [0,0,0,0,0]
			knownGetMailCount, knownLocalSocketTout, knownAlertTemplCache, knownNetWebException, knownGetSafe, knownItemDuplicate = [0,0,0,0,0,0]
			
			knownInputDataErr = int(map(lineStr.find, ['ERROR [Australia Interest Rate(web)] input_OnDataReceive'])[0])  # ERROR [Australia Interest Rate(web)] input_OnDataReceive
			knownStartIndexErr = int(map(lineStr.find, ['StartIndex cannot be less than zero'])[0])  # '2)	ERROR StartIndex cannot be less than zero.'
			knownWarnInputErr = int(map(lineStr.find, ['WARN '])[0])  # 'WARN [Australia Interest Rate(web)] INPUT ERROR'
			knownKeyNotFound = int(map(lineStr.find, ['KeyNotFoundException'])[0])  # 'KeyNotFoundException'
			knownFormatException = int(map(lineStr.find, ['FormatException'])[0])
			knownFailed = int(map(lineStr.find, ['Failed <GBBOEQ'])[0])
			knownSeleniumFirefox = int(map(lineStr.find, ['SeleniumFirefoxWebWatcher'])[0])  # SeleniumFirefoxWebWatcher.cs -> GetPage().
			knownWebDriverException = int(map(lineStr.find, ['WebDriverException'])[0])  # OpenQA.Selenium.WebDriverException: The HTTP request to the remote WebDriver server for URL 
			knownGetMailCount = int(map(lineStr.find, ['GetMailCount'])[0])  # Error happens in Imap4COntroller-->GetMailCount() . ActiveUp.Net.Mail.Imap4Exception: Command "SELECT INBOX" failed : 160201125949965.
			knownLocalSocketTout = int(map(lineStr.find, ['Local socket timeout was'])[0])  # The socket connection was aborted. This could be caused by an error processing your message or a receive timeout being exceeded by the remote host, or an underlying network resource issue. Local socket timeout was '00:04:59.9980000'.. 
			knownAlertTemplCache = int(map(lineStr.find, ['AlertTemplateCache'])[0]) # ERROR [IDNService][AlertTemplateCache] : Exception thrown when updating cache!. 
			knownNetWebException = int(map(lineStr.find, ['System.Net.WebException'])[0]) # ERROR The operation has timed out. System.Net.WebException: The operation has timed out 
			knownGetSafe = int(map(lineStr.find, ['HttpExtension.GetSafeResponse'])[0]) # ERROR [TR.NewsAutomation.Util.HttpExtension]Error occured in HttpExtension.GetSafeResponse().
			knownItemDuplicate = int(map(lineStr.find, ['Item is a duplicate'])[0]) # ERROR [Quantum] Failure : Message sent failed : Item is a duplicate.
			
			alertLevelStr = 'CRITICAL'
			logExtract = "KNOWN ISSUE - " + lineStr[25:265]  # default is Known Issue, till reaches else statement below
				##print "@ knownKeyNotFound @: ",knownKeyNotFound,", sourceLog: ",sourceLog
			if (((knownKeyNotFound > 0) or (knownLocalSocketTout > 0) or (knownAlertTemplCache > 0)) and (('IDNS' in sourceLog) or ('test' in sourceLog))): # 
				alertLevelStr = 'HARMLESS'				
			elif (((knownGetMailCount > 0) or (knownFormatException > 0) or (knownFailed > 0)) and (('Crys' in sourceLog) or ('test' in sourceLog))): # 
				alertLevelStr = 'HARMLESS'
			elif (((knownSeleniumFirefox > 0) or (knownWebDriverException > 0) or (knownNetWebException > 0) or (knownGetSafe > 0) or (knownItemDuplicate > 0) or (knownInputDataErr > 0) or (knownStartIndexErr > 0)) and (('Crys' in sourceLog) or ('test' in sourceLog))): 
				alertLevelStr = 'MINOR'
			elif (knownWarnInputErr > 0): 
				alertLevelStr = 'WARNING'
			else:
				logExtract = lineStr[25:265]  # everything after position 25 - TRACE [Web]APP INFO LOADING....

			##  2015-02-16 09:41:19.8730 TRACE [Web]APP INFO LOADING....			
			file = open(fileGMI, "a+")
			logDateTime = lineStr[0:19] # 2015-02-16 09:41:19
			GetComputerName = socket.gethostname() #'GetComputerName'
			threadCount = '1'  # set a default number as 1, since not sure how to obtain value with python
			pID = "%d" % os.getpid() # return integer as a string, for concatenation purpose
			## ## logExtract = lineStr[25:]  # everything after position 25 - TRACE [Web]APP INFO LOADING....
			logExtract = logExtract.rstrip('\r|\n') # remove line characters
			newStr4GMI = currTimeStamp + "|CBE 1.0.2|" + alertLevelStr + "|" + GetComputerName + "|Hostname|" + logDateTime + " " + logExtract + "|0|LEAP Log Monitor v0.1|Monitor|Process|Web Server|LEAP Log Server|1|" + pID + "|" + threadCount + "|ReportSituation|INTERNAL|STATUS|LEAP_001207|Reuters|0|0|0\n"
			#print " ** CRIT ",newStr4GMI
			#file = open("LEAP_monitor_gmi.log", "a")
			file.write(newStr4GMI) 
			file.close()
			
		else:
			foundInfoWeb,foundInfoAuto,foundInfoWAR,foundInfoAUS,foundInfoQuant = map(lineStr.find, ['[Web]','[Automation]','[WARSAW]','[Australia','sent to Quantum'])  # i.e  [31,-1,-1], '[Web]' found at position 31 no other matches
			foundInfoWeb = int(foundInfoWeb)
			foundInfoAuto = int(foundInfoAuto)
			foundInfoWAR = int(foundInfoWAR)
			foundInfoAUS = int(foundInfoAUS)
			foundInfoQuant = int(foundInfoQuant)

			if ((foundInfoWeb > 0) or (foundInfoAuto > 0) or (foundInfoWAR > 0) or (foundInfoAUS > 0) or (foundInfoQuant > 0)):
				alertLevelStr = 'INFORMATION'
				##  2015-02-16 09:41:19.8730 TRACE [Web]APP INFO LOADING....
				file = open(fileGMI, "a+")
				logDateTime = lineStr[0:19] # 2015-02-16 09:41:19
				GetComputerName = socket.gethostname() #'GetComputerName'
				threadCount = '1'  # set a default number as 1, since not sure how to obtain value with python
				pID = "%d" % os.getpid() # return integer as a string, for concatenation purpose
				logExtract = lineStr[25:265]  # everything after position 25 - TRACE [Web]APP INFO LOADING....
				logExtract = logExtract.rstrip('\r|\n') # remove line characters
				newStr4GMI = currTimeStamp + "|CBE 1.0.2|" + alertLevelStr + "|" + GetComputerName + "|Hostname|" + logDateTime + " " + logExtract + "|0|LEAP Log Monitor v0.1|Monitor|Process|Web Server|LEAP Log Server|1|" + pID + "|" + threadCount + "|ReportSituation|INTERNAL|STATUS|LEAP_001207|Reuters|0|0|0\n"
				#print " ** INFO ",newStr4GMI		  
				file.write(newStr4GMI) 
				file.close()
    
def readlines_then_tail(fin):
	"Iterate through lines and then tail for further lines."
    
	while True:
		line = fin.readline()
		if line:
			yield line
		else:
			tail(fin)

def tail(fin):
	"Listen for new lines added to file."

	while True:
		where = fin.tell()
		line = fin.readline()					

		if not line:
			time.sleep(SLEEP_INTERVAL)
			fin.seek(where)
		else:
			search_file_content(line)			

def main():
	p = OptionParser("usage: leapLog2GMI.py file_to_tail log_choice source_log_dir output_log_dir")
	(options, args) = p.parse_args()
    #print options
	#**  3  :  2  *:*  ['testTailMon.log', '2', '1>D:\\Reuters\\LEAP_Log_Monitor\\logs\\LEAP_mon_CRYS_Scheduler.log 2>>&1']
	##print "** ",len(args), " : ",args[1]," *:* ",args
	lineCount = 0		
	global sourceLogDir, today, outputLogDir, fileGMI, sourceLog
	today = datetime.now() 
	currDate = today.strftime("%Y-%m-%d") # 2015-02-16
	sourceLog = sourceLogDir + "\\" + args[0]        
	searchWARS,searchCRYS,searchDTCA,searchGERM,searchIDNS,searchRDFC,searchTMPL,searchSPAIN = [0,0,0,0,0,0,0,0]
	
	if( len(args) > 1 ):	# i.e. leapLog2GMI.py testLeap.log 1 "C:\\logs" "D:\\Reuters\\LEAP_Log_Monitor\\logs" "1>D:\\Reuters\\LEAP_Log_Monitor\\logs\\LEAP_mon_WARS_Scheduler.log 2>>&1"
		
		if len(args) == 5:
			if(not(args[3]) == ""):
				outputLogDir = args[3]  # "D:\\Reuters\\LEAP_Log_Monitor\\logs"
			if(not(args[2]) == ""):
				sourceLogDir = args[2]  # "D:\\logs"
		elif len(args) == 4:
			if(not(args[3]) == ""):
				outputLogDir = args[3]  # "D:\\Reuters\\LEAP_Log_Monitor\\logs"
			if(not(args[2]) == ""):
				sourceLogDir = args[2]  # "D:\\logs"
		elif len(args) == 3:
			if(not(args[2]) == ""):
				sourceLogDir = args[2]  # "D:\\logs"
		
		###### len(args) > 2 do the below for 3 and above ###############
		# i.e. leapLog2GMI.py testLeap.log 1 "C:\\logs" "D:\\Reuters\\LEAP_Log_Monitor\\logs" "1>D:\\Reuters\\LEAP_Log_Monitor\\logs\\LEAP_mon_WARS_Scheduler.log 2>>&1"
		if(args[1]) == "0":  # testTailMon.log
			fileGMI = outputLogDir + "\\LEAP_monitor_gmi.log"
			##print " IF args1=0 # fileGMI : ",fileGMI,", args3: ", args[3]
			sourceLog = sourceLogDir + "\\" + args[0]   # testTailMon.log
		elif(args[1]) == "1":  # WARSAW
			fileGMI =  outputLogDir + "\\LEAP_mon_WARS_gmi.log"
			sourceLog =  sourceLogDir + "\\Warsaw" + currDate + ".log"   # Warsaw2015-03-03.log
			searchWARS = re.search( r'Warsaw.*', sourceLog, re.M|re.I)
		elif(args[1]) == "2":  # CRYSTAL
			fileGMI =  outputLogDir + "\\LEAP_mon_CRYS_gmi.log"
			sourceLog =  sourceLogDir + "\\Crystal" + currDate + ".log"   # Crystal2015-03-03.log
			searchCRYS = re.search( r'Crystal.*', sourceLog, re.M|re.I)
		elif(args[1]) == "3":  # DTCA
			fileGMI =  outputLogDir + "\\LEAP_mon_DTCA_gmi.log"
			sourceLog =  sourceLogDir + "\\DTCA" + currDate + ".log"   # DTCA2015-03-03.log
			searchDTCA = re.search( r'DTCA.*', sourceLog, re.M|re.I)
		elif(args[1]) == "4":  # GERM
			fileGMI =  outputLogDir + "\\LEAP_mon_GERM_gmi.log"
			sourceLog =  sourceLogDir + "\\GermanBondAuction" + currDate + ".log"   # GermanBondAuction2015-03-03.log
			searchGERM = re.search( r'GermanBondAuction.*', sourceLog, re.M|re.I)
		elif(args[1]) == "5":  # IDNService
			fileGMI =  outputLogDir + "\\LEAP_mon_IDNS_gmi.log" 
			sourceLog =  sourceLogDir + "\\IDNService_MonitoriService" + currDate + ".log" # IDNService_MonitoriService2015-03-03.log
			searchIDNS = re.search( r'IDNService_MonitoriService.*', sourceLog, re.M|re.I)
		elif(args[1]) == "6":  # RDFCom
			fileGMI =  outputLogDir + "\\LEAP_mon_RDFC_gmi.log"
			sourceLog =  sourceLogDir + "\\RDFCommonService" + currDate + ".log"   # RDFCommonService2015-03-03.log
			searchRDFC = re.search( r'RDFCommonService.*', sourceLog, re.M|re.I)
		elif(args[1]) == "7":  # TEMPLATE
			fileGMI =  outputLogDir + "\\LEAP_mon_TMPL_gmi.log"
			sourceLog =  sourceLogDir + "\\TemplateService_RDFReceiver" + currDate + ".log" # TemplateService_RDFReceiver2015-03-03.log
			searchTMPL = re.search( r'TemplateService_RDFReceiver.*', sourceLog, re.M|re.I)
		elif(args[1]) == "8":  # SPANISH
			fileGMI =  outputLogDir + "\\LEAP_mon_SPAIN_gmi.log"
			sourceLog =  sourceLogDir + "\\spbill" + currDate + ".log" # spbill2015-03-03.log
			searchSPAIN = re.search( r'spbill.*', sourceLog, re.M|re.I)
		else:
			fileGMI = outputLogDir + "\\LEAP_monitor_gmi.log"
			sourceLog =  sourceLogDir + args[0]   # testTailMon.log

	## **  2  :  2  *:*  ['testTailMon.log', '2']
	elif(len(args) == 1):   # i.e. leapLog2GMI.py testLeap.log "1>D:\\Reuters\\LEAP_Log_Monitor\\logs\\LEAP_mon_WARS_Scheduler.log 2>>&1"
	# Use specified log name to determine type of file being processed
		searchWARS = re.search( r'Warsaw.*', args[0], re.M|re.I)
		searchCRYS = re.search( r'Crystal.*', args[0], re.M|re.I)
		searchDTCA = re.search( r'DTCA.*', args[0], re.M|re.I)
		searchGERM = re.search( r'GermanBondAuction.*', args[0], re.M|re.I)
		searchIDNS = re.search( r'IDNService_MonitoriService.*', args[0], re.M|re.I)
		searchRDFC = re.search( r'RDFCommonService.*', args[0], re.M|re.I)
		searchTMPL = re.search( r'TemplateService_RDFReceiver.*', args[0], re.M|re.I)
		searchSPAIN = re.search( r'spbill.*', args[0], re.M|re.I)

	##print " *$$* tailFile # sourceLog[",sourceLog,"], fileGMI[",fileGMI,"]"
	tailFile = sourceLog
    
    ##print searchWARS, searchCRYS, searchDTCA, searchGERM, searchIDNS, searchRDFC, searchTMPL
	if searchWARS:  # WARSAW
		fileGMI =  outputLogDir + "\\LEAP_mon_WARS_gmi.log"
	elif searchCRYS:  # CRYSTAL
		fileGMI =  outputLogDir + "\\LEAP_mon_CRYS_gmi.log"
	elif searchDTCA:  # DTCA
		fileGMI =  outputLogDir + "\\LEAP_mon_DTCA_gmi.log"    	   
	elif searchGERM:  # GERM
		fileGMI =  outputLogDir + "\\LEAP_mon_GERM_gmi.log"
	elif searchIDNS:  # IDNService
		fileGMI =  outputLogDir + "\\LEAP_mon_IDNS_gmi.log" 
	elif searchRDFC:  # RDFCom
		fileGMI =  outputLogDir + "\\LEAP_mon_RDFC_gmi.log"
	elif searchTMPL:  # TEMPLATE
		fileGMI =  outputLogDir + "\\LEAP_mon_TMPL_gmi.log"   
	elif searchSPAIN:  # SPAIN
		fileGMI =  outputLogDir + "\\LEAP_mon_SPAIN_gmi.log"   
	else:
		if ('test' not in sourceLog):
			fileGMI = "logs\\LEAP_monitor_gmi.log"
			sourceLog =  args[0]  
			tailFile = args[0] 
			
	##print " # DEFAULT output to LEAP_monitor_gmi.log - sourceLog: ",sourceLog, ", fileGMI: ", fileGMI

	if not os.path.exists(sourceLog):  # if specified file not in logs directory, use specified details as full path
		pass
		print "file [{}] does NOT exist in the specified directory.".format(sourceLog)
		print "TRY: if File in current dir - args0: {}, fileGMI: {}, sourceLog: {}".format(args[0],fileGMI,sourceLog)

		if os.path.exists(args[0]):
			pass
            ##print "File [",args[0],"] exisits in current dir"
			tailFile = args[0] 
			fileGMI = "logs\\LEAP_monitor_gmi.log"
			sourceLog =  args[0] 
		else:
			loopCount = 0
			SLEEP_LENGTH = 3600 # specify seconds to sleep for i.e. 3600 = 1 hour
						
			while not os.path.exists(sourceLog):
				loopCount += 1  # increase loop count
				if( loopCount < 13 ):					
					print "File [{}] not found. Loop Count[{}] entering sleep mode for {} seconds".format(sourceLog,loopCount,SLEEP_LENGTH)
					time.sleep(SLEEP_LENGTH) ## 1 Hour wait
				else:
					print "Exiting Program since source/tail file [{}] is not found.".format(args[0])
					exit(1)			 
    	
	if len(args) < 1:
		print "must specify a file to watch"

	with open(tailFile, 'r') as fin:

	  for lineStr in readlines_then_tail(fin):
		search_file_content(lineStr)

if __name__ == '__main__':
    main()
