from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, is_admin=False, password=None):

        if not email:
            raise ValueError(
                {'message': 'EMAIL_IS_REQUIRED'}
            )

        user = self.model(
            email=self.normalize_email(email),
            is_admin=is_admin
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, is_admin=True, password=None):

        user = self.create_user(
            email=email,
            is_admin=is_admin,
            password=password,
        )
        user.is_active = True
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        # return user