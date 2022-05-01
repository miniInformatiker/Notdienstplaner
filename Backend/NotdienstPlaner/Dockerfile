FROM mcr.microsoft.com/dotnet/aspnet:6.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443
 
ENV ASPNETCORE_ENVIRONMENT=Development

FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY ["Notdienstplaner.csproj", "./"]
RUN dotnet restore "Notdienstplaner.csproj"
COPY . .
WORKDIR "/src/"
RUN dotnet build "Notdienstplaner.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "Notdienstplaner.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "Notdienstplaner.dll"]
