from django.apps import AppConfig


class FlightappConfig(AppConfig):
    name = 'flightapp'

    def ready(self):
        # Automatic superuser creation on startup
        try:
            from django.contrib.auth import get_user_model
            from decouple import config
            User = get_user_model()
            
            SU_USERNAME = config('SUPERUSER_USERNAME', default=None)
            SU_EMAIL = config('SUPERUSER_EMAIL', default=None)
            SU_PASSWORD = config('SUPERUSER_PASSWORD', default=None)
            
            if SU_USERNAME and SU_PASSWORD:
                if not User.objects.filter(username=SU_USERNAME).exists():
                    User.objects.create_superuser(
                        username=SU_USERNAME,
                        email=SU_EMAIL or 'admin@example.com',
                        password=SU_PASSWORD
                    )
                    print(f"--- AUTOMATIC SUPERUSER CREATION SUCCESSFUL: {SU_USERNAME} ---")
                else:
                    print(f"--- Superuser '{SU_USERNAME}' already exists ---")
            else:
                print("--- Automatic superuser creation skipped: SUPERUSER_USERNAME or SUPERUSER_PASSWORD not set in environment variables ---")
        except Exception as e:
            print(f"--- Automatic superuser creation skipped: {e} ---")
