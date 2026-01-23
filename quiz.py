# Welcome to the ehrQL Quiz!

from quiz_answers import questions

from ehrql import codelist_from_csv, show, months
from ehrql.tables.core import clinical_events


diabetes_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dm_cod.csv", column="code"
)
referral_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dsep_cod.csv", column="code"
)
mild_frailty_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-mildfrail_cod.csv", column="code"
)
moderate_frailty_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-modfrail_cod.csv", column="code"
)
severe_frailty_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-sevfrail_cod.csv", column="code"
)
hba1c_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-ifcchbam_cod.csv", column="code"
)

# Question 0
# Create an event frame by filtering clinical_events to find just the records indicating a diabetes
# diagnosis. (Use the diabetes_codes codelist.)
questions[0].check(
    clinical_events.where(clinical_events.snomedct_code.is_in(diabetes_codes))
)

# Question 1
# Create a patient series containing the date of each patient's earliest diabetes diagnosis.
questions[1].check(
        clinical_events
        .where(clinical_events.snomedct_code.is_in(diabetes_codes))
        .sort_by(clinical_events.date)
        .first_for_patient()
        .date
)
# If you need a hint for this, or any other, question, just uncomment (remove the #) from the following line:
# questions[1].hint()

# Question 2
# Create a patient series containing the date of each patient's earliest structured education
# programme referral. (Use the referral_code codelist.)

earliest_referral_date = (
    clinical_events
    .where(clinical_events.snomedct_code.is_in(referral_codes))
    .sort_by(clinical_events.date)
    .first_for_patient()
    .date
)

questions[2].check(earliest_referral_date)
# questions[2].hint()

# Question 3
# Create a boolean patient series indicating whether the date of each patient's earliest diabetes
# diagnosis was between 1st April 2023 and 31st March 2024. If the patient does not have a
# diagnosis, the value for in this series should be False.
earliest_diagnosis_date = (
    clinical_events.where(clinical_events.snomedct_code.is_in(diabetes_codes))
    .sort_by(clinical_events.date)
    .first_for_patient()
    .date
)

# show( 
#    earliest_diagnosis_date.is_not_null() 
#    & earliest_diagnosis_date.is_on_or_between("2023-04-01", "2024-03-31")
#)

questions[3].check(
    earliest_diagnosis_date.is_not_null() 
    & earliest_diagnosis_date.is_on_or_between("2023-04-01", "2024-03-31")
)
# questions[3].hint()

# Question 4
# Create a patient series indicating the number of months between a patient's earliest diagnosis
# and their earliest referral.

date_between_diagnosis_referral = (
    (earliest_referral_date - earliest_diagnosis_date).months
)

# show(date_between_diagnosis_referral)

questions[4].check(date_between_diagnosis_referral)

# questions[4].hint()

# Question 5
# Create a boolean patient series identifying patients who have been diagnosed with diabetes for
# the first time in the year between 1st April 2023 and 31st March 2024, and who have a record of
# being referred to a structured education programme within nine months after their diagnosis.

questions[5].check(
    earliest_referral_date.is_not_null()
    & earliest_diagnosis_date.is_not_null()
    & (earliest_diagnosis_date.is_on_or_between("2023-04-01", "2024-03-31"))
    & (date_between_diagnosis_referral >= 0)
    & (date_between_diagnosis_referral < 9)
)

# questions[5].hint()

# Question 6
# Create a patient series with the date of the latest record of mild frailty for each patient.

latest_mild_frailty = (
    clinical_events
    .where(clinical_events.snomedct_code.is_in(mild_frailty_codes))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .date
)

questions[6].check(latest_mild_frailty)
# questions[6].hint()

# Question 7
# Create a patient series with the date of the latest record of moderate or severe frailty for
# each patient.

mod_sev_frailty_codes = moderate_frailty_codes + severe_frailty_codes

latest_modsev_frailty = (
    clinical_events
    .where(clinical_events.snomedct_code.is_in(mod_sev_frailty_codes))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .date
)

questions[7].check(latest_modsev_frailty)

#questions[7].hint()

# Question 8
# A patient may have mild, moderate and severe frailty codes in their record. A patient's frailty
# is considered to be their most recent frailty code. So if their most recent frailty code was for
# mild frailty, then we would say they have mild frailty.
# Create a boolean patient series indicating whether a patient has moderate or severe frailty, i.e
# where the patient's last record of severity is moderate or severe. If the patient does not have
# a record of frailty, the value in this series should be False.

has_moderate_or_severe_frailty = (
    latest_modsev_frailty.is_not_null()
    & (
        latest_mild_frailty.is_null()
        | (latest_modsev_frailty.is_after(latest_mild_frailty))
    )
)

questions[8].check(has_moderate_or_severe_frailty)

# questions[8].hint()

# Question 9
# Create a patient series containing the latest HbA1c measurement for each patient.

latest_hba1c = (
    clinical_events
    .where(clinical_events.snomedct_code.is_in(hba1c_codes))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .numeric_value
)

questions[9].check(latest_hba1c)
# questions[9].hint()

# Question 10
# Create a boolean patient series identifying patients without moderate or severe frailty in whom
# the last IFCC-HbA1c is 58 mmol/mol or less

hba1c_in_range = (
    ((latest_hba1c) <= 58) 
    & (has_moderate_or_severe_frailty.is_null())
    & latest_hba1c.is_not_null()
)

questions[10].check(hba1c_in_range)
# questions[10].hint()

questions.summarise()
