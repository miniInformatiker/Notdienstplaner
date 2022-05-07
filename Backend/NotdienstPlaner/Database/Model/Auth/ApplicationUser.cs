using Microsoft.AspNetCore.Identity;

namespace Notdienstplaner.Database.Model.Auth;

public class ApplicationUser : IdentityUser
{
    public string FirstName { get; set; }
    public string LastName { get; set; }
    
}