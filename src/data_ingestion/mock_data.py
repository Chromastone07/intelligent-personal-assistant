def fetch_mock_emails():
    """Returns a list of fake email data for development."""
    print("Fetching mock email data...")
    return [
        {
            "subject": "Urgent: Q3 Financial Report Review",
            "from": "boss@company.com",
            "body": "Hi team, please review the attached Q3 financial report and provide your feedback by tomorrow EOD. This is our top priority."
        },
        {
            "subject": "Marketing Campaign Brainstorm",
            "from": "colleague@company.com",
            "body": "Let's schedule a meeting for next Tuesday to brainstorm ideas for the new marketing campaign. Please come prepared with some initial thoughts."
        },
        {
            "subject": "FWD: Weekly Project Update",
            "from": "project-manager@company.com",
            "body": "Here is the weekly update. The deadline for the user testing phase is approaching on September 15th."
        }
    ]