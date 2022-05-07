using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Notdienstplaner.Migrations
{
    public partial class AddApplicationUser : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DeleteData(
                table: "AspNetRoles",
                keyColumn: "Id",
                keyValue: "55437fde-871d-4c3f-a167-11d54d916f77");

            migrationBuilder.InsertData(
                table: "AspNetRoles",
                columns: new[] { "Id", "ConcurrencyStamp", "Name", "NormalizedName" },
                values: new object[] { "28d7076f-d786-4c0f-a930-9a6aaf368f93", "e37fc3fb-f633-4b5f-a455-f8f3c7268ccb", "Admin", "ADMIN" });
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DeleteData(
                table: "AspNetRoles",
                keyColumn: "Id",
                keyValue: "28d7076f-d786-4c0f-a930-9a6aaf368f93");

            migrationBuilder.InsertData(
                table: "AspNetRoles",
                columns: new[] { "Id", "ConcurrencyStamp", "Name", "NormalizedName" },
                values: new object[] { "55437fde-871d-4c3f-a167-11d54d916f77", "ca9e30e7-b764-4fb9-807d-d28eba258ea5", "Admin", "ADMIN" });
        }
    }
}
