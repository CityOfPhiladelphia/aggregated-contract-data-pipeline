0. Get the filenames

   ```bash
   ls data/FY16Q3/*.2016_Contract_Extract_PW_Payments.xls
   ```

1. Use `csvkit` to convert excel files to CSV, e.g.:

   ```bash
   in2csv data/FY16Q3/01.2016_Contract_Extract_PW_Payments.xls
   ```

2. Combine the PW data into one file and the SSE data into another

   ```bash
   csvstack ... ... ...
   ```

3. Create an aggregated file for each

   ```bash
   aggregate-contracts pw ...
   aggregate-contracts sse ...
   ```

4. Combine the two resulting files

   ```bash
   csvstack ... ...
   ```

5. Upload the combined data to GitHub


## Sample commands:

``bash
csvstack <(in2csv data/FY16Q4/04.2016Contract_Extract_PW_Payments.xls) \
         <(in2csv data/FY16Q4/05.2016_Contract_Extract_PW_Payments.xls) \
         <(in2csv data/FY16Q4/06.2016_Contract_Extract_PW_Payments.xls) \
  | aggregate-contracts pw | csvlook | less -S

csvstack <(in2csv data/FY16Q4/04.2016_ContractRenewal_Payments.xls) \
         <(in2csv data/FY16Q4/05.2016_ContractRenewal_Payments.xls) \
         <(in2csv data/FY16Q4/06.2016_ContractRenewal_Payments.xls) \
  | aggregate-contracts sse | csvlook | less -S
```
