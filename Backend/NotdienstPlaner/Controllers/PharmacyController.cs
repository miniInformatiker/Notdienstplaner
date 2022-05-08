using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Notdienstplaner.Database;
using Notdienstplaner.Database.Model;

namespace Notdienstplaner.Controllers;

[Authorize]
[Route("api/[controller]")]
[ApiController]
public class PharmacyController : ControllerBase
{
    private readonly ApplicationDbContext _context;

    public PharmacyController(ApplicationDbContext context)
    {
        _context = context;
    }

    // GET: api/Pharmacy
    [HttpGet]
    public async Task<ActionResult<IEnumerable<Pharmacy>>> GetPharmacies()
    {
        return await _context.Pharmacies.ToListAsync();
    }

    // GET: api/Pharmacy/5
    [HttpGet("{id}")]
    public async Task<ActionResult<Pharmacy>> GetPharmacy(Guid id)
    {
        var pharmacy = await _context.Pharmacies.FindAsync(id);

        if (pharmacy == null) return NotFound();

        return pharmacy;
    }

    // PUT: api/Pharmacy/5
    // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
    [HttpPut("{id}")]
    public async Task<IActionResult> PutPharmacy(Guid id, Pharmacy pharmacy)
    {
        if (id != pharmacy.Id) return BadRequest();

        _context.Entry(pharmacy).State = EntityState.Modified;

        try
        {
            await _context.SaveChangesAsync();
        }
        catch (DbUpdateConcurrencyException)
        {
            if (!PharmacyExists(id))
                return NotFound();
            throw;
        }

        return NoContent();
    }

    // POST: api/Pharmacy
    // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
    [HttpPost]
    public async Task<ActionResult<PharmacyController>> PostPharmacy(Pharmacy pharmacy)
    {
        _context.Pharmacies.Add(pharmacy);
        await _context.SaveChangesAsync();

        return CreatedAtAction("GetPharmacy", new { id = pharmacy.Id }, pharmacy);
    }

    // DELETE: api/Pharmacy/5
    [HttpDelete("{id}")]
    public async Task<IActionResult> DeletePharmacy(Guid id)
    {
        var pharmacy = await _context.Pharmacies.FindAsync(id);
        if (pharmacy == null) return NotFound();

        _context.Pharmacies.Remove(pharmacy);
        await _context.SaveChangesAsync();

        return NoContent();
    }

    private bool PharmacyExists(Guid id)
    {
        return _context.Pharmacies.Any(e => e.Id == id);
    }
}