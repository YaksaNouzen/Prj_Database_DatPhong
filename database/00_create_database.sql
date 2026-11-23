-- Chạy trên instance SQL Server dành cho đồ án.
USE [master];
GO

IF DB_ID(N'HotelBooking') IS NULL
BEGIN
    EXEC(N'CREATE DATABASE [HotelBooking];');
END;
GO

USE [HotelBooking];
GO

SELECT DB_NAME() AS database_name;
GO
