# slash_automation_test

## Install following libraries

```
pip install undetected_chromedriver dotenv selenium pytest hashlib
```

## Run test

Add testcase to /pages directory.
Add .env file

Specify testcases in an json file. 
See sample file: sample_amounts.json

Run:

```
python test_full_payment_flow.py --env YOUR_SPECIFIED_ENV --amounts YOUR_DESIRED_AMOUNTS_CONFIG_FILE --by WHO_SET_THE_AMOUNT
```

Sample parameter values:
  - YOUR_SPECIFIED_ENV: LOCAL, STG, PREMAIN, TESTNET, MAINNET
  - YOUR_DESIRED_AMOUNTS_CONFIG_FILE: sample_amounts.json
  - WHO_SET_THE_AMOUNT: merchant, payer

Sample command:

```
python test_full_payment_flow.py --env LOCAL --amounts sample_amounts.json --by payer
```
