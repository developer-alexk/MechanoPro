from django.db import models

class Rattings(models.Model):
    rating = models.IntegerField(default=0)
    comment = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('users.Account', on_delete=models.CASCADE)
    company = models.ForeignKey('users.Company', on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

#Logic for the ratings calculation
def calculate_rating(company_id):
    ratings = Rattings.objects.filter(company_id=company_id)
    total_rating = 0
    for rating in ratings:
        total_rating += rating.rating
    #if there are no ratings, return 0
    if len(ratings) == 0:
        return 0
    return total_rating/len(ratings)