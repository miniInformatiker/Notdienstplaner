using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Notdienstplaner.Database.Model;

public class Pharmacy
{
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    [Key]
    public Guid Id { get; set; }

    public string Name { get; set; }

    public string Email { get; set; }

    public string Phone { get; set; }

    public string Place { get; set; }

    public string Street { get; set; }

    public string Housenumber { get; set; }
    
    public string Postcode { get; set; }

}