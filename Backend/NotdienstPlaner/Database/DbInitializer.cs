using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Notdienstplaner.Database.Model.Auth;

namespace Notdienstplaner.Database;

public static class DbInitializer
{
    public static void SeedUsers(ApplicationDbContext context, UserManager<ApplicationUser> userManager)
    {
        if (userManager.FindByEmailAsync("malte@friedrich-burhave.de").Result != null) 
            return;
        
        var user = new ApplicationUser
        {
            UserName = "Admin",
            FirstName = "Malte",
            LastName = "Friedrich",
            Email = "malte@friedrich-burhave.de",
            EmailConfirmed = true,
            PhoneNumberConfirmed = true,
            NormalizedUserName = "ADMIN",
            NormalizedEmail = "MALTE@FRIEDRICH-BURHAVE.DE"
        };

        var passwordHasher = new PasswordHasher<ApplicationUser>();
        var passwordHash = passwordHasher.HashPassword(user, "Start:123");

        user.PasswordHash = passwordHash;

        var userStore = new UserStore<ApplicationUser>(context);

        userStore.CreateAsync(user).Wait();
    }
}