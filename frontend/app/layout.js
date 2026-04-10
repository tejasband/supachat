export const metadata = {
  title: "SupaChat AI",
  description: "Conversational Analytics App",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
