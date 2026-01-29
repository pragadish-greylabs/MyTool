#Ptp (Promise to pay) Date validation
#“01-02-2026”
#Valid _date = 7
#Current date 29-01-2026
#user mentiond - 01-02-2026
#Diff = 3 days
#if  difff <=7 
    #Valid
#else 
    #Invalid
#filters
#past date
#parse date

import logging
from datetime import date , datetime 
from pydantic import BaseModel ,Field
from langchain_core.tools import tool
from typing import Dict , Any , Optional 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PTP:
    """
    this is the class where we check the given date by the customer according to the following rules:
    1. it shldnt be in the past 
    2. it shld be in the future
    3. it shldnt exceed above 7 days from today
    """

    #def __init__(self,userDate:Optional[str]):
    
    def tool_for_checkPTP(self):
        logger.info("creating a tool for date validation")

        class Schema(BaseModel):
            dateVariable : Optional[str] = Field(default = None , description = "this is the variable for our date ")

        @tool("checkPTP",description = "use this tool to check whether the date is not in the past and also the date is within 7 days from today",args_schema = Schema)
        def checkPTP(dateVariable:Optional[str]=None)->Dict[Any,Any]:
            """
            this is where we check whether it is a past date or future and also check if it is within the 7 day timeline 
            """
            logger.info("starting to check the validation")
            #dateVariable = dateVariable

            
            try:
                today = date.today()
                if dateVariable is None or dateVariable.strip()=="":
                    return {
                        "status":"failed",
                        "response":"the input is empty"
                    }
                convertDate=datetime.strptime(dateVariable, "%d-%m-%Y").date()

                if today > convertDate:
                    return {
                        "status":"failed",
                        "response":"the given date is not valid , it is in the past"
                    }
                
                diff = (convertDate - today).days

                if diff>7:
                    return {
                        "status":"failed",
                        "response":f"the given date is exceeding the limit of 7 days , it is {diff} days from today"
                    }
                
                return {
                    "status":"success",
                    "response":f"{convertDate} is a valid date , please proceed....."
                }
            
            except Exception as e:
                logger.error("ERROR ERROR ERROR")
                return {
                    "status":"error",
                    "response":f"we are facing this error - {e}"
                }
            
        return checkPTP
            

if __name__ == "__main__":
    instance = PTP()
    toolll = instance.tool_for_checkPTP()

    result = toolll.invoke({
        "dateVariable":"08-01-2026"
    })

    print(result)


