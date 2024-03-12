from datetime import datetime, timedelta

def schedule_case(case_type, last_hearing_date):
    try:
        # Ensure the date format matches the expected format
        last_date = datetime.strptime(last_hearing_date, "%Y-%m-%d")

        # Your scheduling logic here...
        scheduled_date = last_date + timedelta(days=7)

        return [{'case_type': case_type, 'scheduled_date': scheduled_date.strftime('%Y-%m-%d')}]

    except ValueError as e:
        print(f"Error in schedule_case: {e}")
        return None  # Handle the error accordingly
